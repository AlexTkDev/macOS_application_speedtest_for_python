import os
import json
import logging
from datetime import datetime
from tkinter import Toplevel, Text, Scrollbar, messagebox, ttk, Frame, Button
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Получаем логгер
logger = logging.getLogger("SpeedTest")

# Path to the file for storing history
HISTORY_FILE = "test_history.json"


def save_test_results(download_speed, upload_speed, ping, file_path="test_history.json"):
    """Saves the test results to a specified JSON file with timestamp."""
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "download_speed": download_speed,
        "upload_speed": upload_speed,
        "ping": ping
    }

    # If the file exists, load the current data
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
    try:
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
        logger.error(f"Error decoding JSON from {history_path}")
        messagebox.showerror("Error", "Could not read history file. It may be corrupted.")
        return
    except Exception as e:
        logger.error(f"Error reading history file: {e}", exc_info=True)
        messagebox.showerror("Error", f"Could not read history file: {e}")
        return

    # Create a new window to display the history
    history_window = Toplevel(root)
    history_window.title("Test History")
    history_window.geometry("600x400")
    history_window.minsize(600, 400)

    # Create a frame for the treeview and scrollbar
    frame = Frame(history_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a Treeview widget
    columns = ("index", "timestamp", "download", "upload", "ping")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Define headings
    tree.heading("index", text="#")
    tree.heading("timestamp", text="Timestamp")
    tree.heading("download", text="Download (Mbps)")
    tree.heading("upload", text="Upload (Mbps)")
    tree.heading("ping", text="Ping (ms)")

    # Define column widths
    tree.column("index", width=50)
    tree.column("timestamp", width=150)
    tree.column("download", width=120)
    tree.column("upload", width=120)
    tree.column("ping", width=100)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Populate the treeview
    for idx, entry in enumerate(history, start=1):
        timestamp = entry.get("timestamp", "N/A")
        tree.insert("", "end", values=(
            idx,
            timestamp,
            entry["download_speed"],
            entry["upload_speed"],
            entry["ping"]
        ))

    # Add an export button
    def export_csv():
        """Export history data to CSV file."""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export History to CSV"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("Index,Timestamp,Download (Mbps),Upload (Mbps),Ping (ms)\n")
                    for idx, entry in enumerate(history, start=1):
                        timestamp = entry.get("timestamp", "N/A")
                        f.write(
                            f"{idx},{timestamp},{entry['download_speed']},{entry['upload_speed']},{entry['ping']}\n")
                messagebox.showinfo("Export", f"History exported to {file_path}")
                logger.info(f"History exported to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting history: {e}", exc_info=True)
            messagebox.showerror("Export Error", f"Could not export history: {e}")

    # Add buttons at the bottom
    button_frame = Frame(history_window)
    button_frame.pack(fill="x", padx=10, pady=5)

    export_button = Button(button_frame, text="Export to CSV", command=export_csv)
    export_button.pack(side="left", padx=5)

    close_button = Button(button_frame, text="Close", command=history_window.destroy)
    close_button.pack(side="right", padx=5)


def plot_history(root, history_path):
    """Plots the history of the tests with an interactive matplotlib window."""
    if not os.path.exists(history_path):
        messagebox.showinfo("History", "No history available.")
        return

    try:
        with open(history_path, "r", encoding="utf-8") as file:
            history = json.load(file)
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {history_path}")
        messagebox.showerror("Error", "Could not read history file. It may be corrupted.")
        return
    except Exception as e:
        logger.error(f"Error reading history file: {e}", exc_info=True)
        messagebox.showerror("Error", f"Could not read history file: {e}")
        return

    # Get data for the plot
    download_speeds = [entry["download_speed"] for entry in history]
    upload_speeds = [entry["upload_speed"] for entry in history]
    pings = [entry["ping"] for entry in history]
    tests = range(1, len(history) + 1)

    # Extract timestamps if available
    timestamps = []
    for entry in history:
        if "timestamp" in entry:
            timestamps.append(entry["timestamp"])
        else:
            # If no timestamp, use the test number
            timestamps.append(f"Test {len(timestamps) + 1}")

    # Create plot window
    plot_window = Toplevel(root)
    plot_window.title("Speed Test History Graph")
    plot_window.geometry("800x600")
    plot_window.minsize(800, 600)

    # Create matplotlib figure and axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

    # Plot speeds on the first axes
    ax1.plot(tests, download_speeds, label="Download Speed (Mbps)", marker="o", color="green")
    ax1.plot(tests, upload_speeds, label="Upload Speed (Mbps)", marker="s", color="blue")
    ax1.set_xlabel("Test Number")
    ax1.set_ylabel("Speed (Mbps)")
    ax1.set_title("Internet Speed Test History")
    ax1.legend()
    ax1.grid(True)

    # Plot ping on the second axes
    ax2.plot(tests, pings, label="Ping (ms)", marker="^", color="red")
    ax2.set_xlabel("Test Number")
    ax2.set_ylabel("Ping (ms)")
    ax2.legend()
    ax2.grid(True)

    # Adjust layout
    plt.tight_layout()

    # Create a frame to hold the plot
    plot_frame = Frame(plot_window)
    plot_frame.pack(fill="both", expand=True)

    # Add the plot to the frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Add toolbar
    toolbar_frame = Frame(plot_window)
    toolbar_frame.pack(fill="x")
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

    # Add button frame
    button_frame = Frame(plot_window)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Add close button
    close_button = Button(button_frame, text="Close", command=plot_window.destroy)
    close_button.pack(side="right", padx=5)

    # Add save button
    def save_plot():
        """Save the plot to a file."""
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
                logger.info(f"Plot saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving plot: {e}", exc_info=True)
            messagebox.showerror("Save Error", f"Could not save plot: {e}")

    save_button = Button(button_frame, text="Save Plot", command=save_plot)
    save_button.pack(side="left", padx=5)