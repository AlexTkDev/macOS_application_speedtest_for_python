### On development stage. 
## Documentation for macOS_application_speedtest_for_python

### Project Description
`macOS_application_speedtest_for_python` is a modern macOS application for testing your internet connection speed using Python. The app features a beautiful dark UI (ttkbootstrap), asynchronous and thread-based architecture for maximum responsiveness, and advanced UX with toast notifications and smooth progress animations.

### What's New in Version 4.0.0
- Fully asynchronous and thread-based architecture: all heavy operations (speedtest, network info, plotting) run in background threads.
- Modern, dark, and airy UI using ttkbootstrap.
- Toast notifications for test completion and errors.
- Smooth progress bar animations and non-blocking interface.
- Improved error handling and logging.
- Refactored codebase: all comments and docstrings in English, modular structure.
- Enhanced test history and export features.
- More robust PyInstaller build and troubleshooting section.

### Installation

#### System Requirements
- macOS (version 10.14 or later)
- Python 3.8 or higher (with Tkinter support)
- All dependencies from `requirements.txt`

#### Installing Dependencies
```bash
# Clone repository
git clone https://github.com/AlexTkDev/macOS_application_speedtest_for_python.git
cd macOS_application_speedtest_for_python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
Run the application:
```bash
python main.py
```
Or build the .app:
```bash
pyinstaller main.spec
open dist/Alex_SpeedTest.app
```

#### Features
- **Asynchronous Speed Test**: Download, upload, and ping tests run in a background thread.
- **Modern Dark UI**: Built with ttkbootstrap for a beautiful, modern look.
- **Toast Notifications**: Non-blocking popups for test completion and errors.
- **Network Adapter Info**: Asynchronously fetches and displays active network adapter details.
- **Interactive History & Graphs**: View and export your test history, plot interactive graphs.
- **Export to CSV**: Export your test history for further analysis.
- **Logging**: All actions are logged for troubleshooting.

#### Project Structure
```
macOS_application_speedtest_for_python/
├── speedtest_app/             # Main package
│   ├── __init__.py            # Package initialization
│   ├── alexs_speedtest.py     # Main application module (async, threads)
│   ├── network_adapter_information.py   # Async network info
│   ├── test_history.py        # Async history and plotting
│   ├── gui/                   # GUI components (ttkbootstrap)
│   │   └── __init__.py
│   ├── utils/                 # Utility functions
│   │   └── __init__.py
│   └── tests/                 # Unit tests
│       ├── __init__.py
│       ├── test_network_adapter.py
│       └── test_test_history.py
├── main.py                    # Entry point
├── main.spec                  # PyInstaller config
├── requirements.txt           # Dependencies
├── setup.py                   # Installation script
├── README.md                  # This documentation
```

### How It Works
1. Click **Start Speed Test** to run a speed test in a background thread.
2. The app finds the best server, runs the test, and updates the UI with smooth progress.
3. Results are shown instantly; you can repeat the test, view/export history, or plot interactive graphs.
4. All network info and history operations are also asynchronous.
5. Toast notifications inform you of completion or errors.

### Building the Application
To build the application in `.app` format:
```bash
pyinstaller main.spec
```
The `.app` will appear in the `dist` directory.

#### Troubleshooting PyInstaller/macOS
- If the app does not open, run the binary from terminal to see errors:
  ```bash
  dist/Alex_SpeedTest.app/Contents/MacOS/alexs_speedtest
  ```
- If you see `ModuleNotFoundError: No module named '_tkinter'`, ensure your Python has Tkinter support and rebuild the venv.
- If macOS blocks the app, run:
  ```bash
  xattr -dr com.apple.quarantine dist/Alex_SpeedTest.app
  ```
- For other issues, check the log file in `~/Documents/SpeedTest_Logs/speedtest_log.log`.

### Running Tests
```bash
python -m unittest discover
```

### License
MIT License. See `LICENSE` for details.

### Contribution
Pull requests are welcome! See CONTRIBUTING section in the old README for workflow.

### Contact
For questions or suggestions, reach out via [GitHub](https://github.com/AlexTkDev).