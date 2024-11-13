import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import speedtest as st
import network_adapter_information


def update_progress(value, message):
    """Updates the progress bar and message."""
    progress_bar['value'] = value
    progress_label.config(text=f"{message} (Progress: {value}%)")
    root.update_idletasks()  # Update the interface


def perform_speedtest():
    """Performs the speed test and updates the UI with results."""
    test = st.Speedtest()
    result_container = {}

    # Download speed test
    update_progress(0, "Starting download speed test...")
    download_thread = threading.Thread(target=test_download_speed, args=(test, result_container))
    download_thread.start()
    download_thread.join()  # Wait for the download test to finish

    if 'error' in result_container:
        messagebox.showerror("Error", result_container['error'])
        return

    download_speed = result_container['download']

    # Upload speed test
    update_progress(0, "Starting upload speed test...")
    upload_thread = threading.Thread(target=test_upload_speed, args=(test, result_container))
    upload_thread.start()
    upload_thread.join()  # Wait for the upload test to finish

    if 'error' in result_container:
        messagebox.showerror("Error", result_container['error'])
        return

    upload_speed = result_container['upload']
    ping = test.results.ping

    display_results(download_speed, upload_speed, ping)


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

    # Show "Repeat Speed Test" button and hide the exit button
    repeat_button.pack(pady=10)


def start_speedtest():
    """Starts the speed test when the button is pressed."""
    result_label.config(text="Running speed test...")
    start_button.pack_forget()  # Hide the start button
    repeat_button.pack_forget()  # Hide the repeat button if it was visible

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


def exit_program():
    """Closes the program."""
    root.quit()


# Create main window
root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("400x450")

# Button to start speed test
start_button = tk.Button(root, text="Start Speed Test", command=start_speedtest)
start_button.pack(pady=20)

# Button to repeat speed test
repeat_button = tk.Button(root, text="Repeat Speed Test", command=start_speedtest)
repeat_button.pack_forget()  # Initially hidden

# Label to display results
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Label to display progress
progress_label = tk.Label(root, text="")
# Initially, progress is not visible

# Progress bar
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
# Initially, progress is not visible

# Label to display system information
system_info_label = tk.Label(root, text="", justify="left", anchor="w")
system_info_label.pack(pady=10, padx=20)

# Exit button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(side="bottom", pady=10)

# Run the application
root.mainloop()
