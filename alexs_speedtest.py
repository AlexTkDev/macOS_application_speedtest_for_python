import os
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import speedtest as st
import network_adapter_information
from test_history import save_test_results, view_history, plot_history


# Get the history file path in the Documents folder
def get_history_path():
    """Returns the path to the history file in the Documents folder."""
    home = os.path.expanduser("~")
    documents_path = os.path.join(home, "Documents")
    os.makedirs(documents_path, exist_ok=True)  # Creates the folder if it doesn't exist
    return os.path.join(documents_path, "test_history.json")


# Path to the history file
history_path = get_history_path()


def update_progress(value, message):
    """Updates the progress bar and message."""
    progress_bar['value'] = value
    progress_label.config(text=f"{message} (Progress: {value}%)")
    root.update_idletasks()  # Update the interface


def perform_speedtest():
    """Performs the speed test and updates the UI with results."""
    try:
        test = st.Speedtest()
        result_container = {}

        # Download speed test
        update_progress(0, "Starting download speed test...")
        download_thread = threading.Thread(target=test_download_speed,
                                           args=(test, result_container))
        download_thread.start()
        download_thread.join()  # Wait for the download test to finish

        if 'error' in result_container:
            raise ValueError(result_container['error'])

        download_speed = result_container['download']

        # Upload speed test
        update_progress(0, "Starting upload speed test...")
        upload_thread = threading.Thread(target=test_upload_speed, args=(test, result_container))
        upload_thread.start()
        upload_thread.join()  # Wait for the upload test to finish

        if 'error' in result_container:
            raise ValueError(result_container['error'])

        upload_speed = result_container['upload']
        ping = test.results.ping

        display_results(download_speed, upload_speed, ping)

    except st.ConfigRetrievalError as e:
        # Catch speedtest specific errors and show in UI
        messagebox.showerror("Speedtest Error",
                             f"Error retrieving configuration: {e}")
    except Exception as e:
        # Catch any other exceptions and show in UI
        messagebox.showerror("Error", f"An error occurred: {e}")


def test_download_speed(test, result_container):
    """Tests download speed."""
    try:
        download_speed = test.download(callback=download_progress_callback)
        if download_speed is None:
            raise ValueError("Download speed test did not return a valid speed.")
        result_container['download'] = round(download_speed / 10 ** 6, 2)  # Convert to Mbps
    except Exception as e:
        result_container['error'] = f"Download speed test error: {str(e)}"


def test_upload_speed(test, result_container):
    """Tests upload speed."""
    try:
        upload_speed = test.upload(callback=upload_progress_callback)
        if upload_speed is None:
            raise ValueError("Upload speed test did not return a valid speed.")
        result_container['upload'] = round(upload_speed / 10 ** 6, 2)  # Convert to Mbps
    except Exception as e:
        result_container['error'] = f"Upload speed test error: {str(e)}"


def download_progress_callback(current, total, **kwargs):
    """Updates progress during the download speed test."""
    if total > 0:  # Avoid division by zero
        percentage = int((current / total) * 100)
        update_progress(percentage, "Testing download speed...")


def upload_progress_callback(current, total, **kwargs):
    """Updates progress during the upload speed test."""
    if total > 0:  # Avoid division by zero
        percentage = int((current / total) * 100)
        update_progress(percentage, "Testing upload speed...")


def display_results(down_speed, up_speed, ping):
    """Displays the results of the speed test in the interface."""
    result_text = (
        f"Download speed: {down_speed} Mbps\n"
        f"Upload speed: {up_speed} Mbps\n"
        f"Ping: {ping} ms"
    )
    result_label.config(text=result_text)
    update_progress(100, "Test complete!")  # Set progress to 100%

    # Hide the progress bar after the test is complete
    progress_label.pack_forget()
    progress_bar.pack_forget()

    # Save results to history
    save_test_results(down_speed, up_speed, ping, history_path)

    # Show "Repeat Speed Test" button and hide the exit button
    repeat_button.pack(pady=10)

    # Show history buttons after the test is complete
    history_frame.pack(pady=10)


def start_speedtest():
    """Starts the speed test when the button is pressed."""
    result_label.config(text="Running speed test...")
    start_button.pack_forget()  # Hide the start button
    repeat_button.pack_forget()  # Hide the repeat button if it was visible

    # Hide history buttons when repeating the test
    history_frame.pack_forget()

    # Show progress bar
    progress_label.pack(pady=10)
    progress_bar.pack(pady=20)

    # Start the speed test in a separate thread
    threading.Thread(target=perform_speedtest).start()

    # Get and display system information
    display_system_info()


def display_system_info():
    """Displays system information in the interface."""
    info = network_adapter_information.get_network_info()

    info_text = f"Computer Name: {info['Computer Name']}"
    info_text += "\nAdapters:\n"

    for adapter in info['Adapters']:
        info_text += f"- Adapter: {adapter['Adapter']}\n"
        info_text += f"- IP Address: {adapter['IP Address']}\n"
        info_text += f"- MAC Address: {adapter['MAC Address']}\n"

    system_info_label.config(text=info_text)


def repeat_speedtest():
    """Repeats the speed test."""
    result_label.config(text="Running speed test again...")
    history_frame.pack_forget()  # Hide history buttons before repeating the test

    # Hide the progress bar before repeating the test
    progress_label.pack_forget()
    progress_bar.pack_forget()

    start_speedtest()  # Restart the test


def exit_program():
    """Closes the program."""
    root.quit()


# Create main window
root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("400x450")

# Label to display system information
system_info_label = tk.Label(root, text="", justify="left", anchor="w")
system_info_label.pack(pady=10, padx=20)

# Button to start speed test
start_button = tk.Button(root, text="Start Speed Test", command=start_speedtest)
start_button.pack(pady=20)

# Button to repeat speed test
repeat_button = tk.Button(root, text="Repeat Speed Test", command=start_speedtest)
repeat_button.pack_forget()  # Initially hidden
repeat_button.config(command=repeat_speedtest)  # Connect the new function to the button

# Label to display results
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Label to display progress
progress_label = tk.Label(root, text="")
# Initially, progress is not visible

# Progress bar
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
# Initially, progress is not visible

# Create frame for history buttons
history_frame = tk.Frame(root)

# Button to view history
history_button = tk.Button(history_frame, text="View Test History table",
                           command=lambda: view_history(root, history_path))
history_button.pack(side="left", padx=10)

plot_button = tk.Button(history_frame, text="Show graph Test History",
                        command=lambda: plot_history(root, history_path))
plot_button.pack(side="left", padx=10)

# Hide the history frame until the test is complete
history_frame.pack_forget()

# Exit button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(side="bottom", pady=10)

# Run the application
root.mainloop()
