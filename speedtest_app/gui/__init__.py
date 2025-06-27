"""
GUI components for macOS_application_speedtest_for_python.
"""
import ttkbootstrap as tb
import tkinter as tk
from tkinter import messagebox, Menu
import logging

logger = logging.getLogger("SpeedTest")


class ResultsFrame(tb.Frame):
    """Frame for displaying speed test results (modern, dark, airy)."""

    def __init__(self, master, **kwargs):
        super().__init__(master, padding=20, **kwargs)
        font_title = ("Segoe UI", 16, "bold")
        font_label = ("Segoe UI", 12)
        font_value = ("Segoe UI", 12, "bold")

        self.result_title = tb.Label(self, text="Test Results", font=font_title)
        self.result_title.pack(pady=(10, 15))

        # Download speed result
        self.download_row = tb.Frame(self)
        self.download_row.pack(fill="x", pady=6)
        self.download_label = tb.Label(self.download_row, text="Download:", font=font_label, width=15, anchor="w")
        self.download_label.pack(side="left", padx=5)
        self.download_value = tb.Label(self.download_row, text="-- Mbps", font=font_value, width=15, anchor="e")
        self.download_value.pack(side="left", padx=5)

        # Upload speed result
        self.upload_row = tb.Frame(self)
        self.upload_row.pack(fill="x", pady=6)
        self.upload_label = tb.Label(self.upload_row, text="Upload:", font=font_label, width=15, anchor="w")
        self.upload_label.pack(side="left", padx=5)
        self.upload_value = tb.Label(self.upload_row, text="-- Mbps", font=font_value, width=15, anchor="e")
        self.upload_value.pack(side="left", padx=5)

        # Ping result
        self.ping_row = tb.Frame(self)
        self.ping_row.pack(fill="x", pady=6)
        self.ping_label = tb.Label(self.ping_row, text="Ping:", font=font_label, width=15, anchor="w")
        self.ping_label.pack(side="left", padx=5)
        self.ping_value = tb.Label(self.ping_row, text="-- ms", font=font_value, width=15, anchor="e")
        self.ping_value.pack(side="left", padx=5)

        # Timestamp
        self.timestamp_row = tb.Frame(self)
        self.timestamp_row.pack(fill="x", pady=6)
        self.timestamp_label = tb.Label(self.timestamp_row, text="Test Time:", font=font_label, width=15, anchor="w")
        self.timestamp_label.pack(side="left", padx=5)
        self.timestamp_value = tb.Label(self.timestamp_row, text="--", font=font_value, width=25, anchor="e")
        self.timestamp_value.pack(side="left", padx=5)

        self.pack_forget()

    def update_results(self, download, upload, ping, timestamp):
        """Updates the result values."""
        self.download_value.config(text=f"{download} Mbps")
        self.upload_value.config(text=f"{upload} Mbps")
        self.ping_value.config(text=f"{ping} ms")
        self.timestamp_value.config(text=timestamp)
        self.pack(fill="both", expand=True, pady=10)

    def clear(self):
        """Clears the result values."""
        self.download_value.config(text="-- Mbps")
        self.upload_value.config(text="-- Mbps")
        self.ping_value.config(text="-- ms")
        self.timestamp_value.config(text="--")


class SettingsWindow:
    """Window for application settings (modern, dark, airy)."""

    def __init__(self, parent, settings, save_callback):
        self.parent = parent
        self.settings = settings
        self.save_callback = save_callback
        self.window = tb.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.window.geometry(f"+{x}+{y}")
        self.frame = tb.Frame(self.window, padding=30)
        self.frame.pack(fill="both", expand=True)
        self.auto_save_var = tk.BooleanVar(value=settings.get("auto_save_results", True))
        self.auto_save_check = tb.Checkbutton(
            self.frame,
            text="Automatically save test results",
            variable=self.auto_save_var
        )
        self.auto_save_check.pack(anchor="w", pady=10)
        self.show_network_var = tk.BooleanVar(value=settings.get("show_network_info", True))
        self.show_network_check = tb.Checkbutton(
            self.frame,
            text="Show network adapter information",
            variable=self.show_network_var
        )
        self.show_network_check.pack(anchor="w", pady=10)
        self.dark_mode_var = tk.BooleanVar(value=settings.get("dark_mode", True))
        self.dark_mode_check = tb.Checkbutton(
            self.frame,
            text="Dark mode (requires restart)",
            variable=self.dark_mode_var
        )
        self.dark_mode_check.pack(anchor="w", pady=10)
        self.button_frame = tb.Frame(self.window)
        self.button_frame.pack(fill="x", padx=30, pady=20)
        self.save_button = tb.Button(
            self.button_frame,
            text="Save",
            command=self.save_settings
        )
        self.save_button.pack(side="right", padx=5)
        self.cancel_button = tb.Button(
            self.button_frame,
            text="Cancel",
            command=self.window.destroy
        )
        self.cancel_button.pack(side="right", padx=5)

    def save_settings(self):
        """Saves the settings and closes the window."""
        self.settings["auto_save_results"] = self.auto_save_var.get()
        self.settings["show_network_info"] = self.show_network_var.get()
        self.settings["dark_mode"] = self.dark_mode_var.get()

        if self.save_callback:
            self.save_callback(self.settings)

        self.window.destroy()


def create_menu(root, settings_callback, about_callback):
    """Creates the application menu bar."""
    menubar = Menu(root)

    # File menu
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Settings", command=settings_callback)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # Tools menu
    tools_menu = Menu(menubar, tearoff=0)
    tools_menu.add_command(label="Export All History", command=lambda: messagebox.showinfo(
        "Feature Coming Soon", "This feature will be available in the next update."
    ))
    tools_menu.add_command(label="Clear History", command=lambda: messagebox.showinfo(
        "Feature Coming Soon", "This feature will be available in the next update."
    ))
    menubar.add_cascade(label="Tools", menu=tools_menu)

    # Help menu
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="View Help", command=lambda: messagebox.showinfo(
        "Help",
        "For help and documentation, please visit: https://github.com/AlexTkDev/"
        "macOS_application_speedtest_for_python"
    ))
    help_menu.add_separator()
    help_menu.add_command(label="About", command=about_callback)
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)

    return menubar


def show_about_dialog(parent):
    """Shows the About dialog."""
    from speedtest_app import __version__

    about_window = tb.Toplevel(parent)
    about_window.title("About Internet Speed Test")
    about_window.geometry("300x200")
    about_window.resizable(False, False)
    about_window.transient(parent)
    about_window.grab_set()

    # Center on parent
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (300 // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (200 // 2)
    about_window.geometry(f"+{x}+{y}")

    # App name and version
    app_name = tb.Label(about_window, text="Internet Speed Test", font=("Segoe UI", 16, "bold"))
    app_name.pack(pady=(20, 5))

    version = tb.Label(about_window, text=f"Version {__version__}")
    version.pack()

    # Separator
    separator = tb.Separator(about_window, orient="horizontal")
    separator.pack(fill="x", padx=20, pady=10)

    # Developer info
    dev_info = tb.Label(about_window, text="Developed by Aleksandr")
    dev_info.pack()

    # Copyright info
    copyright_info = tb.Label(about_window, text="© 2024 Aleksandr. MIT License")
    copyright_info.pack()

    # Close button
    close_button = tb.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=20)