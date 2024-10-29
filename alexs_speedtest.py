import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import speedtest as st


def update_progress(value, message):
    """Updates the progress bar and message label."""
    progress_bar['value'] = value
    progress_label.config(text=f"{message} (Progress: {value}%)")
    root.update_idletasks()  # Update the GUI


def perform_speedtest():
    """Performs the speed test and updates the UI with results."""
    test = st.Speedtest()
    result_container = {}

    # Start download speed test
    update_progress(0, "Starting download speed test...")
    download_thread = threading.Thread(target=test_download_speed, args=(test, result_container))
    download_thread.start()
    download_thread.join()  # Wait for the download thread to finish

    if 'error' in result_container:
        messagebox.showerror("Error", result_container['error'])
        return

    download_speed = result_container['download']

    # Prepare for upload speed test
    update_progress(0, "Starting upload speed test...")
    upload_thread = threading.Thread(target=test_upload_speed, args=(test, result_container))
    upload_thread.start()
    upload_thread.join()  # Wait for the upload thread to finish

    if 'error' in result_container:
        messagebox.showerror("Error", result_container['error'])
        return

    upload_speed = result_container['upload']
    ping = test.results.ping

    display_results(download_speed, upload_speed, ping)


def test_download_speed(test, result_container):
    """Tests download speed and stores the result in the result_container."""
    try:
        download_speed = test.download(callback=download_progress_callback)
        if download_speed is None:
            raise ValueError("Download speed test did not return a valid speed.")
        result_container['download'] = round(download_speed / 10 ** 6, 2)  # Convert to Mbps
    except Exception as e:
        result_container['error'] = f"Download speed test error: {str(e)}"


def test_upload_speed(test, result_container):
    """Tests upload speed and stores the result in the result_container."""
    try:
        upload_speed = test.upload(callback=upload_progress_callback)
        if upload_speed is None:
            raise ValueError("Upload speed test did not return a valid speed.")
        result_container['upload'] = round(upload_speed / 10 ** 6, 2)  # Convert to Mbps
    except Exception as e:
        result_container['error'] = f"Upload speed test error: {str(e)}"


def download_progress_callback(current, total, **kwargs):
    """Callback to update progress during download speed test."""
    if total > 0:  # Avoid division by zero
        percentage = int((current / total) * 100)
        update_progress(percentage, "Testing download speed...")


def upload_progress_callback(current, total, **kwargs):
    """Callback to update progress during upload speed test."""
    if total > 0:  # Avoid division by zero
        percentage = int((current / total) * 100)
        update_progress(percentage, "Testing upload speed...")


def display_results(down_speed, up_speed, ping):
    """Displays the speed test results in the UI."""
    result_text = (
        f"Download speed: {down_speed} Mbps\n"
        f"Upload speed: {up_speed} Mbps\n"
        f"Ping: {ping} ms"
    )
    result_label.config(text=result_text)
    update_progress(100, "Test complete!")  # Set progress bar to 100%

    # Show "Repeat Speed Test" button and hide the exit button
    repeat_button.pack(pady=10)


def start_speedtest():
    """Starts the speed test when the button is pressed."""
    result_label.config(text="Running speed test...")
    start_button.pack_forget()  # Hide the start button
    repeat_button.pack_forget()  # Hide the repeat button if it was visible

    # Run the speed test in a separate thread
    threading.Thread(target=perform_speedtest).start()


def exit_program():
    """Exits the application."""
    root.quit()


# Create the main window
root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("400x400")

# Create the start button
start_button = tk.Button(root, text="Start Speed Test", command=start_speedtest)
start_button.pack(pady=20)

# Create a repeat button that will be shown after the first test
repeat_button = tk.Button(root, text="Repeat Speed Test", command=start_speedtest)
repeat_button.pack_forget()  # Initially hide the repeat button

# Create a label to display results
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Create a label to show progress
progress_label = tk.Label(root, text="")
progress_label.pack(pady=10)

# Create a progress bar
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=20)

# Create a button to exit the program
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(pady=10)

# Run the application
root.mainloop()
