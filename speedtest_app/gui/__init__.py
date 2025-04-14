"""
GUI components for macOS_application_speedtest_for_python.
"""
import tkinter as tk
from tkinter import ttk, messagebox, Menu
import logging

logger = logging.getLogger("SpeedTest")


class ResultsFrame(tk.Frame):
    """Frame for displaying speed test results."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create labels for results
        self.result_title = tk.Label(self, text="Test Results", font=("Helvetica", 14, "bold"))
        self.result_title.pack(pady=(10, 5))

        # Download speed result
        self.download_frame = tk.Frame(self)
        self.download_frame.pack(fill="x", pady=2)

        self.download_label = tk.Label(self.download_frame, text="Download Speed:", width=15,
                                       anchor="w")
        self.download_label.pack(side="left", padx=5)

        self.download_value = tk.Label(self.download_frame, text="-- Mbps", width=15, anchor="e")
        self.download_value.pack(side="left", padx=5)

        # Upload speed result
        self.upload_frame = tk.Frame(self)
        self.upload_frame.pack(fill="x", pady=2)

        self.upload_label = tk.Label(self.upload_frame, text="Upload Speed:", width=15, anchor="w")
        self.upload_label.pack(side="left", padx=5)

        self.upload_value = tk.Label(self.upload_frame, text="-- Mbps", width=15, anchor="e")
        self.upload_value.pack(side="left", padx=5)

        # Ping result
        self.ping_frame = tk.Frame(self)
        self.ping_frame.pack(fill="x", pady=2)

        self.ping_label = tk.Label(self.ping_frame, text="Ping:", width=15, anchor="w")
        self.ping_label.pack(side="left", padx=5)

        self.ping_value = tk.Label(self.ping_frame, text="-- ms", width=15, anchor="e")
        self.ping_value.pack(side="left", padx=5)

        # Timestamp
        self.timestamp_frame = tk.Frame(self)
        self.timestamp_frame.pack(fill="x", pady=2)

        self.timestamp_label = tk.Label(self.timestamp_frame, text="Test Time:", width=15,
                                        anchor="w")
        self.timestamp_label.pack(side="left", padx=5)

        self.timestamp_value = tk.Label(self.timestamp_frame, text="--", width=25, anchor="e")
        self.timestamp_value.pack(side="left", padx=5)

        # Initially hide
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
    """Window for application settings."""

    def __init__(self, parent, settings, save_callback):
        self.parent = parent
        self.settings = settings
        self.save_callback = save_callback

        # Create a new window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.window.geometry(f"+{x}+{y}")

        # Create a frame for settings
        self.frame = tk.Frame(self.window, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        # Auto save results
        self.auto_save_var = tk.BooleanVar(value=settings.get("auto_save_results", True))
        self.auto_save_check = ttk.Checkbutton(
            self.frame,
            text="Automatically save test results",
            variable=self.auto_save_var
        )
        self.auto_save_check.pack(anchor="w", pady=5)

        # Show network info
        self.show_network_var = tk.BooleanVar(value=settings.get("show_network_info", True))
        self.show_network_check = ttk.Checkbutton(
            self.frame,
            text="Show network adapter information",
            variable=self.show_network_var
        )
        self.show_network_check.pack(anchor="w", pady=5)

        # Dark mode option
        self.dark_mode_var = tk.BooleanVar(value=settings.get("dark_mode", False))
        self.dark_mode_check = ttk.Checkbutton(
            self.frame,
            text="Dark mode (requires restart)",
            variable=self.dark_mode_var
        )
        self.dark_mode_check.pack(anchor="w", pady=5)

        # Create buttons
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(fill="x", padx=20, pady=20)

        self.save_button = ttk.Button(
            self.button_frame,
            text="Save",
            command=self.save_settings
        )
        self.save_button.pack(side="right", padx=5)

        self.cancel_button = ttk.Button(
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

    about_window = tk.Toplevel(parent)
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
    app_name = tk.Label(about_window, text="Internet Speed Test", font=("Helvetica", 16, "bold"))
    app_name.pack(pady=(20, 5))

    version = tk.Label(about_window, text=f"Version {__version__}")
    version.pack()

    # Separator
    separator = ttk.Separator(about_window, orient="horizontal")
    separator.pack(fill="x", padx=20, pady=10)

    # Developer info
    dev_info = tk.Label(about_window, text="Developed by Aleksandr")
    dev_info.pack()

    # Copyright info
    copyright_info = tk.Label(about_window, text="© 2024 Aleksandr. MIT License")
    copyright_info.pack()

    # Close button
    close_button = ttk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=20)