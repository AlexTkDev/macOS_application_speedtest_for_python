import os
import json
import logging
from datetime import datetime
from tkinter import Toplevel, Text, Scrollbar, messagebox, ttk, Frame, Button
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
import concurrent.futures
import tkinter.messagebox as messagebox

logger = logging.getLogger("SpeedTest")


def get_history_file_path():
    """Returns the path to the history file in Downloads directory."""
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    return os.path.join(downloads_dir, "speedtest_history.json")


def save_test_results(download_speed, upload_speed, ping, file_path=None):
    """Saves the test results to the Downloads directory."""
    if file_path is None:
        file_path = get_history_file_path()

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "download_speed": download_speed,
        "upload_speed": upload_speed,
        "ping": ping
    }

    try:
        # Ensure directory exists (although Downloads should always exist)
        downloads_dir = os.path.dirname(file_path)
        if not os.path.exists(downloads_dir):
            logger.warning(f"Downloads directory not found at {downloads_dir}")
            messagebox.showerror("Error", "Downloads directory not found")
            return

        # Load existing history or create new
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    history = json.load(file)
            except json.JSONDecodeError:
                logger.error(f"Error decoding JSON from {file_path}. Creating new history.")
                history = []
        else:
            history = []

        # Add new data
        history.append(data)

        # Save the updated file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)
        logger.info(f"Test results saved to {file_path}")

    except Exception as e:
        logger.error(f"Error saving test results: {e}", exc_info=True)
        messagebox.showerror("Error", f"Could not save test results: {e}")


def view_history(root, history_path):
    """Opens a new window with the test history using a Treeview widget."""
    if not os.path.exists(history_path):
        messagebox.showinfo("History", "No history available.")
        return

    try:
        with open(history_path, "r", encoding="utf-8") as file:
            history = json.load(file)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Could not read history file. It may be corrupted.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Could not read history file: {e}")
        return

    history_window = tb.Toplevel(root)
    history_window.title("Test History")
    history_window.geometry("650x450")
    history_window.minsize(650, 450)
    frame = tb.Frame(history_window, padding=20)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    columns = ("#", "Timestamp", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)")
    data = [
        [idx, entry.get("timestamp", "N/A"), entry["download_speed"], entry["upload_speed"], entry["ping"]]
        for idx, entry in enumerate(history, start=1)
    ]
    table = Tableview(
        master=frame,
        coldata=columns,
        rowdata=data,
        paginated=False,
        searchable=False,
        bootstyle="darkly",
        autofit=True,
        stripecolor=("#23272b", "#343a40")
    )
    table.pack(fill="both", expand=True)
    def export_csv():
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export History to CSV"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(",".join(columns) + "\n")
                    for row in data:
                        f.write(",".join(str(x) for x in row) + "\n")
                messagebox.showinfo("Export", f"History exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export history: {e}")
    button_frame = tb.Frame(history_window)
    button_frame.pack(fill="x", padx=10, pady=10)
    export_button = tb.Button(button_frame, text="Export to CSV", command=export_csv)
    export_button.pack(side="left", padx=5)
    close_button = tb.Button(button_frame, text="Close", command=history_window.destroy)
    close_button.pack(side="right", padx=5)


def plot_history(root, history_path):
    if not os.path.exists(history_path):
        messagebox.showinfo("History", "No history available.")
        return

    loading_win = tb.Toplevel(root)
    loading_win.title("Loading Plot...")
    loading_win.geometry("350x120")
    loading_win.resizable(False, False)
    loading_label = tb.Label(loading_win, text="Building plot, please wait...", font=("Segoe UI", 13))
    loading_label.pack(expand=True, pady=30)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def build_plot_data():
        try:
            with open(history_path, "r", encoding="utf-8") as file:
                history = json.load(file)
            download_speeds = [entry["download_speed"] for entry in history]
            upload_speeds = [entry["upload_speed"] for entry in history]
            pings = [entry["ping"] for entry in history]
            tests = range(1, len(history) + 1)
            timestamps = [entry.get("timestamp", f"Test {i+1}") for i, entry in enumerate(history)]
            return (download_speeds, upload_speeds, pings, tests, timestamps)
        except Exception as e:
            return e

    def on_plot_ready(result):
        loading_win.destroy()
        if isinstance(result, Exception):
            messagebox.showerror("Plot Error", f"Could not build plot: {result}")
            return
        download_speeds, upload_speeds, pings, tests, timestamps = result
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        ax1.plot(tests, download_speeds, label="Download Speed (Mbps)", marker="o", color="#00bc8c")
        ax1.plot(tests, upload_speeds, label="Upload Speed (Mbps)", marker="s", color="#375a7f")
        ax1.set_xlabel("Test Number")
        ax1.set_ylabel("Speed (Mbps)")
        ax1.set_title("Internet Speed Test History", fontsize=14)
        ax1.legend()
        ax1.grid(True, color="#444")
        ax2.plot(tests, pings, label="Ping (ms)", marker="^", color="#f39c12")
        ax2.set_xlabel("Test Number")
        ax2.set_ylabel("Ping (ms)")
        ax2.legend()
        ax2.grid(True, color="#444")
        plt.tight_layout()
        plot_window = tb.Toplevel(root)
        plot_window.title("Speed Test History Graph")
        plot_window.geometry("850x650")
        plot_window.minsize(850, 650)
        plot_frame = tb.Frame(plot_window)
        plot_frame.pack(fill="both", expand=True)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        toolbar_frame = tb.Frame(plot_window)
        toolbar_frame.pack(fill="x")
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        button_frame = tb.Frame(plot_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        def save_plot():
            try:
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title="Save Plot"
                )
                if file_path:
                    fig.savefig(file_path, dpi=300, bbox_inches="tight")
                    messagebox.showinfo("Save", f"Plot saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save plot: {e}")
        save_button = tb.Button(button_frame, text="Save Plot", command=save_plot)
        save_button.pack(side="left", padx=5)
        close_button = tb.Button(button_frame, text="Close", command=plot_window.destroy)
        close_button.pack(side="right", padx=5)

    future = executor.submit(build_plot_data)
    def check_future():
        if future.done():
            result = future.result()
            root.after(0, lambda: on_plot_ready(result))
        else:
            root.after(100, check_future)
    check_future()
