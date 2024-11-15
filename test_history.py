import json
import os
from tkinter import Toplevel, Text, Scrollbar, messagebox
from matplotlib import pyplot as plt


# Path to the file for storing history
HISTORY_FILE = "test_history.json"


def save_test_results(download_speed, upload_speed, ping, file_path="test_history.json"):
    """Saves the test results to a specified JSON file."""
    data = {
        "download_speed": download_speed,
        "upload_speed": upload_speed,
        "ping": ping
    }

    # If the file exists, load the current data
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            history = json.load(file)
    else:
        history = []

    # Add new data
    history.append(data)

    # Save the updated file
    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)


def view_history(root, history_path):
    """Opens a new window with the test history."""
    if not os.path.exists(history_path):
        messagebox.showinfo("History", "No history available.")
        return

    with open(history_path, "r") as file:
        history = json.load(file)

    # Create a new window to display the history
    history_window = Toplevel(root)
    history_window.title("Test History")
    history_window.geometry("400x400")

    # Add a text area with scroll
    text_area = Text(history_window, wrap="word")
    scrollbar = Scrollbar(history_window, command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Populate the text area with data
    for idx, entry in enumerate(history, start=1):
        text_area.insert(
            "end",
            f"Test {idx}:\n"
            f"  Download Speed: {entry['download_speed']} Mbps\n"
            f"  Upload Speed: {entry['upload_speed']} Mbps\n"
            f"  Ping: {entry['ping']} ms\n\n"
        )

    text_area.config(state="disabled")  # Make the text read-only


def plot_history(root, history_path):
    """Plots the history of the tests."""
    if not os.path.exists(history_path):
        messagebox.showinfo("History", "No history available.")
        return

    with open(history_path, "r") as file:
        history = json.load(file)

    # Get data for the plot
    download_speeds = [entry["download_speed"] for entry in history]
    upload_speeds = [entry["upload_speed"] for entry in history]
    pings = [entry["ping"] for entry in history]
    tests = range(1, len(history) + 1)

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(tests, download_speeds, label="Download Speed (Mbps)", marker="o")
    plt.plot(tests, upload_speeds, label="Upload Speed (Mbps)", marker="o")
    plt.plot(tests, pings, label="Ping (ms)", marker="o")
    plt.xlabel("Test Number")
    plt.ylabel("Value")
    plt.title("Internet Speed Test History")
    plt.legend()
    plt.grid(True)
    plt.show()
