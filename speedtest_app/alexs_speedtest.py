import os
import threading
import logging
import tkinter as tk
from tkinter import ttk, messagebox
import speedtest as st
from datetime import datetime
from speedtest_app import network_adapter_information
from speedtest_app.test_history import save_test_results
from speedtest_app.gui import (
    ResultsFrame,
    SettingsWindow,
    create_menu,
    show_about_dialog
)
from speedtest_app.utils import (
    get_app_version,
    format_speed,
    load_settings,
    save_settings
)
import ttkbootstrap as tb
from speedtest_app.speedtest_service import SpeedTestService
from speedtest_app.network_adapter_information import NetworkInfoService


def setup_logging():
    """
    Configures the logging system for the application.
    """
    log_dir = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        "SpeedTest_Logs"
    )
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "speedtest_log.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("SpeedTest")


class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Internet Speed Test v{get_app_version()}")
        self.root.geometry("400x600")
        self.root.minsize(400, 600)
        self.settings = load_settings()
        create_menu(
            self.root,
            lambda: self.show_settings(),
            lambda: show_about_dialog(self.root)
        )
        # Сначала сервисы!
        self.speedtest_service = SpeedTestService()
        self.test_future = None
        self.network_info_service = NetworkInfoService()
        self.network_info_future = None
        self.setup_gui()
        logger.info("Application initialized")

    def setup_gui(self):
        """Настраивает интерфейс приложения."""
        self.network_info_frame = tb.Frame(self.root)
        if self.settings.get("show_network_info", True):
            self.network_info_frame.pack(fill="x", padx=20, pady=10)
            self.update_network_info()

        self.results_frame = ResultsFrame(self.root)

        self.progress_frame = tb.Frame(self.root)
        self.progress_label = tb.Label(self.progress_frame, text="", font=("Segoe UI", 12))
        self.progress_bar = tb.Progressbar(
            self.progress_frame,
            length=300,
            mode='determinate'
        )

        # Основная рамка для кнопок
        self.button_frame = tb.Frame(self.root)
        self.button_frame.pack(pady=20)

        # Кнопка запуска теста
        self.start_button = tb.Button(
            self.button_frame,
            text="Start Speed Test",
            command=self.start_speedtest,
            width=22
        )
        self.start_button.pack(pady=(0, 8))

        # Кнопка повтора теста (изначально скрыта)
        self.repeat_button = tb.Button(
            self.button_frame,
            text="Repeat Speed Test",
            command=self.repeat_speedtest,
            width=22
        )

        # Кнопки истории и графика (отображаются сразу)
        self.history_button = tb.Button(
            self.button_frame,
            text="Посмотреть историю",
            command=self.show_history,
            width=22
        )
        self.history_button.pack(pady=8)

        self.plot_button = tb.Button(
            self.button_frame,
            text="Посмотреть график",
            command=self.show_plot,
            width=22
        )
        self.plot_button.pack(pady=8)

    def update_network_info(self):
        """Асинхронно обновляет информацию о сетевом адаптере с индикатором загрузки."""
        for widget in self.network_info_frame.winfo_children():
            widget.destroy()
        loading_label = tb.Label(self.network_info_frame, text="Loading network info...", font=("Segoe UI", 11))
        loading_label.pack()
        self.network_info_future = self.network_info_service.get_active_adapter_async()
        self.root.after(100, self._check_network_info_result, loading_label)

    def _check_network_info_result(self, loading_label):
        if self.network_info_future and self.network_info_future.done():
            adapter_info = self.network_info_future.result()
            loading_label.destroy()
            if adapter_info:
                info_text = (
                    f"Adapter: {adapter_info['Adapter']}\n"
                    f"IP: {adapter_info['IP Address']}\n"
                    f"MAC: {adapter_info['MAC Address']}"
                )
                tb.Label(self.network_info_frame, text=info_text, justify="left", font=("Segoe UI", 11)).pack()
            else:
                tb.Label(self.network_info_frame, text="No active network adapter found", font=("Segoe UI", 11)).pack()
        else:
            self.root.after(100, self._check_network_info_result, loading_label)

    def show_settings(self):
        """Показывает окно настроек."""
        SettingsWindow(self.root, self.settings, self.save_settings)

    def save_settings(self, new_settings):
        """Сохраняет настройки."""
        self.settings = new_settings
        save_settings(self.settings)

        if self.settings.get("show_network_info"):
            self.network_info_frame.pack(fill="x", padx=20, pady=10)
            self.update_network_info()
        else:
            self.network_info_frame.pack_forget()

    def start_speedtest(self):
        """Запускает тест скорости (асинхронно через SpeedTestService) с анимацией прогресс-бара."""
        if self.test_future and not self.test_future.done():
            return
        self.results_frame.clear()
        self.progress_frame.pack(pady=10)
        self.progress_label.pack()
        self.progress_bar.pack()
        self.progress_bar["value"] = 0
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start(10)
        self.start_button.config(state="disabled")
        self.repeat_button.pack_forget()
        self.progress_label.config(text="Finding best server...")
        self.test_future = self.speedtest_service.run_speedtest()
        self.root.after(100, self._check_speedtest_result)

    def repeat_speedtest(self):
        """Повторяет тест скорости."""
        self.start_speedtest()

    def _check_speedtest_result(self):
        if self.test_future and self.test_future.done():
            self.progress_bar.stop()
            self.progress_bar.config(mode="determinate")
            result = self.test_future.result()
            if "error" in result:
                self._show_error(result["error"])
                self._cleanup()
            else:
                download = result["download"]
                upload = result["upload"]
                ping = result["ping"]
                self.progress_bar["value"] = 100
                self.progress_label.config(text="Test completed!")
                self._update_results(download, upload, ping)
                self._show_toast("Speed test completed!", "success")
                self._cleanup()
        else:
            self.root.after(100, self._check_speedtest_result)

    def _update_results(self, download, upload, ping):
        """Обновляет интерфейс с результатами теста."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_frame.update_results(
            format_speed(download),
            format_speed(upload),
            f"{ping:.1f}",
            timestamp
        )

        # Показываем кнопку повтора после завершения теста
        self.repeat_button.pack(pady=(5, 0))

        if self.settings.get("auto_save_results", True):
            save_test_results(download, upload, ping)
            logger.info("Test results saved to Downloads directory")

    def _show_error(self, error_message):
        """Показывает сообщение об ошибке."""
        messagebox.showerror("Error", f"Test failed: {error_message}")

    def _cleanup(self):
        """Очищает интерфейс после теста."""
        self.progress_frame.pack_forget()
        self.start_button.config(state="normal")

    def show_history(self):
        """Открывает окно истории тестов."""
        from speedtest_app.test_history import get_history_file_path, view_history
        history_path = get_history_file_path()
        view_history(self.root, history_path)

    def show_plot(self):
        """Открывает окно графика истории тестов."""
        from speedtest_app.test_history import get_history_file_path, plot_history
        history_path = get_history_file_path()
        plot_history(self.root, history_path)

    def _show_toast(self, message, style="info"):
        toast = tb.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        x = self.root.winfo_x() + self.root.winfo_width() - 250
        y = self.root.winfo_y() + 40
        toast.geometry(f"220x40+{x}+{y}")
        frame = tb.Frame(toast)
        frame.pack(fill="both", expand=True)
        label = tb.Label(frame, text=message, font=("Segoe UI", 11))
        label.pack(fill="both", expand=True, padx=10, pady=5)
        toast.after(2000, toast.destroy)


def main():
    """Основная точка входа в приложение."""
    root = tb.Window(themename="darkly")
    app = SpeedTestApp(root)

    try:
        root.mainloop()
    except Exception as e:
        logger.critical(f"Unhandled exception in main loop: {e}", exc_info=True)
        messagebox.showerror("Critical Error", f"An unhandled error occurred: {e}")


if __name__ == "__main__":
    logger = setup_logging()
    main()
