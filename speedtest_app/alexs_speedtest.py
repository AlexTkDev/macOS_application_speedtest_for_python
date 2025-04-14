import os
import threading
import logging
import tkinter as tk
from tkinter import ttk, messagebox
import speedtest as st
from datetime import datetime
from speedtest_app import network_adapter_information
from speedtest_app.test_history import save_test_results, view_history, plot_history
from speedtest_app.gui import ResultsFrame, SettingsWindow, create_menu, show_about_dialog
from speedtest_app.utils import (
    get_app_version,
    format_speed,
    load_settings,
    save_settings,
    ensure_user_data_dir
)


def setup_logging():
    """Настраивает систему логирования."""
    log_dir = os.path.join(os.path.expanduser("~"), "Documents", "SpeedTest_Logs")
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

        self.setup_gui()

        self.speedtest = None
        self.test_thread = None

        logger.info("Application initialized")

    def setup_gui(self):
        """Настраивает интерфейс приложения."""
        self.network_info_frame = tk.Frame(self.root)
        if self.settings.get("show_network_info", True):
            self.network_info_frame.pack(fill="x", padx=20, pady=10)
            self.update_network_info()

        self.results_frame = ResultsFrame(self.root)

        self.progress_frame = tk.Frame(self.root)
        self.progress_label = tk.Label(self.progress_frame, text="")
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=300,
            mode='determinate'
        )

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.start_button = ttk.Button(
            self.button_frame,
            text="Start Speed Test",
            command=self.start_speedtest
        )
        self.start_button.pack()

        self.repeat_button = ttk.Button(
            self.button_frame,
            text="Repeat Speed Test",
            command=self.repeat_speedtest
        )

    def update_network_info(self):
        """Обновляет информацию о сетевом адаптере."""
        adapter_info = network_adapter_information.get_active_adapter_info()
        if adapter_info:
            info_text = (
                f"Adapter: {adapter_info['Adapter']}\n"
                f"IP: {adapter_info['IP Address']}\n"
                f"MAC: {adapter_info['MAC Address']}"
            )
            for widget in self.network_info_frame.winfo_children():
                widget.destroy()
            tk.Label(self.network_info_frame, text=info_text, justify="left").pack()

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
        """Запускает тест скорости."""
        if self.test_thread and self.test_thread.is_alive():
            return

        self.results_frame.clear()

        self.progress_frame.pack(pady=10)
        self.progress_label.pack()
        self.progress_bar.pack()
        self.progress_bar["value"] = 0

        self.start_button.config(state="disabled")

        self.test_thread = threading.Thread(target=self._run_speedtest)
        self.test_thread.start()

    def repeat_speedtest(self):
        """Повторяет тест скорости."""
        self.start_speedtest()

    def _run_speedtest(self):
        """Выполняет тест в отдельном потоке."""
        try:
            self.speedtest = st.Speedtest()

            self.progress_label.config(text="Finding best server...")
            self.progress_bar["value"] = 10
            self.speedtest.get_best_server()

            self.progress_label.config(text="Testing download speed...")
            self.progress_bar["value"] = 30
            download_speed = self.speedtest.download() / 1_000_000

            self.progress_label.config(text="Testing upload speed...")
            self.progress_bar["value"] = 60
            upload_speed = self.speedtest.upload() / 1_000_000

            self.progress_label.config(text="Measuring ping...")
            self.progress_bar["value"] = 90
            ping = self.speedtest.results.ping

            self.progress_bar["value"] = 100
            self.progress_label.config(text="Test completed!")

            self.root.after(0, self._update_results, download_speed, upload_speed, ping)

        except Exception as e:
            logger.error(f"Speed test failed: {e}", exc_info=True)
            self.root.after(0, self._show_error, str(e))
        finally:
            self.root.after(0, self._cleanup)

    def _update_results(self, download, upload, ping):
        """Обновляет интерфейс с результатами теста."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_frame.update_results(
            format_speed(download),
            format_speed(upload),
            f"{ping:.1f}",
            timestamp
        )

        self.repeat_button.pack(pady=(5, 0))

        if self.settings.get("auto_save_results", True):
            save_test_results(download, upload, ping)

    def _show_error(self, error_message):
        """Показывает сообщение об ошибке."""
        messagebox.showerror("Error", f"Test failed: {error_message}")

    def _cleanup(self):
        """Очищает интерфейс после теста."""
        self.progress_frame.pack_forget()
        self.start_button.config(state="normal")


def main():
    """Основная точка входа в приложение."""
    root = tk.Tk()
    app = SpeedTestApp(root)

    try:
        root.mainloop()
    except Exception as e:
        logger.critical(f"Unhandled exception in main loop: {e}", exc_info=True)
        messagebox.showerror("Critical Error", f"An unhandled error occurred: {e}")


if __name__ == "__main__":
    logger = setup_logging()
    main()
