## Documentation for macOS_application_speedtest_for_python

### Project Description
`macOS_application_speedtest_for_python` is a macOS application designed to test your internet connection 
speed using Python. The program provides a convenient interface for measuring download, upload, and ping speeds, 
and also supports retesting and viewing test history.

This project is built based on another one of my applications, which you can check out on GitHub:
[Internet Speed Test](https://github.com/AlexTkDev/different_mini-apps/tree/main/check_internrt_speed)

### What's New in Version 2.0.1
- Added comprehensive logging system for better debugging
- Improved error handling throughout the application
- Enhanced visualization of test history with interactive graphs
- Added export functionality for test history data
- Better network adapter information collection
- Improved progress reporting during tests
- Added unit tests for core functionality
- Reorganized project structure for better maintainability

### Installation

#### System Requirements
- macOS (version 10.14 or later)
- Python 3.6 or higher
- Installed dependencies listed in `requirements.txt`

#### Installing Dependencies
To install the dependencies, execute the following commands:

```bash
# Clone repository
git clone https://github.com/AlexTkDev/macOS_application_speedtest_for_python.git
cd macOS_application_speedtest_for_python

# Method 1: Using requirements.txt
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt

# Method 2: Installing as a package (development mode)
pip install -e .
```

### Usage
After installation, you can run the application by executing:
```bash
# If installed using requirements.txt
python alexs_speedtest.py

# If installed as a package
python -m speedtest_app
```

#### Features
- **Internet Speed Measurement**: The app allows you to test download and upload speeds, as well as ping (latency) of your internet connection.
- **Graphical Display**: After completing a test, users can view the test results and optionally plot the test history.
- **Interactive Graphs**: View your speed test history as interactive graphs with the ability to zoom and navigate.
- **Export Data**: Export your test history to CSV format for further analysis.
- **Detailed Network Information**: View comprehensive information about your network adapters.
- **Repeat Test**: After a test is completed, users can repeat the test without needing to restart the application.
- **Logging System**: The application now logs all activities to help with troubleshooting.

#### Key Components
- **Tkinter**: Used for creating the graphical user interface (GUI), which includes buttons for starting tests, viewing results, and plotting graphs.
- **Speedtest-cli**: A library for performing internet speed tests, which powers the app's functionality.
- **Matplotlib**: A library for visualizing the test history by plotting interactive graphs.
- **JSON**: A library for reading and writing test results stored in JSON format.
- **Logging**: Python's built-in logging module for tracking application behavior.
- **Psutil**: For retrieving system and network adapter information.

#### Project Structure
```
macOS_application_speedtest_for_python/
├── speedtest_app/             # Main package
│   ├── __init__.py            # Package initialization
│   ├── alexs_speedtest.py     # Main application module
│   ├── network_adapter_information.py   # Network info module
│   ├── test_history.py        # History management module
│   ├── gui/                   # GUI components
│   │   └── __init__.py
│   ├── utils/                 # Utility functions
│   │   └── __init__.py
│   └── tests/                 # Unit tests
│       ├── __init__.py
│       ├── test_network_adapter.py
│       └── test_test_history.py
├── main.py                    # Entry point script
├── setup.py                   # Installation script
├── requirements.txt           # Dependencies
├── .pylintrc                  # Pylint configuration
├── .github/workflows/         # GitHub Actions configuration
│   └── pylint.yml
├── LICENSE                    # MIT License
└── README.md                  # This documentation
```

#### How It Works
1. When the app is launched, users can click the **"Start Speed Test"** button to initiate the test.
2. The app first finds the best server, then runs a speed test using the **speedtest-cli** library, measuring download speed, upload speed, and ping.
3. Once the test is completed, the results are displayed in the app's interface.
4. Users can save the test results to the **history.json** file and visualize the data using **matplotlib**'s interactive graphs.
5. For a repeat test, users can simply click the **"Repeat Speed Test"** button, which hides the history buttons until the new test is finished.
6. All application activities are logged to a file in the user's Documents folder for troubleshooting.

#### Building the Application
To build the application in `.app` format, run the following command:
```bash
pyinstaller main.spec
```
After building, the application will be located in the `dist` directory, and you can launch it by double-clicking the icon.

### Configuration
The project includes several configuration files:
- `.pylintrc`: Contains settings for the Pylint code analysis tool
- `main.spec`: Configuration for PyInstaller to build the macOS application

### Running Tests
The project includes unit tests to ensure functionality. To run the tests:
```bash
# Run all tests
python -m unittest discover

# Run specific test module
python -m unittest speedtest_app.tests.test_network_adapter
```

### License
This project is licensed under the MIT License. Please refer to the `LICENSE` file for more detailed information.

### Code Analysis with Pylint
This project uses **Pylint** for static code analysis to ensure that code adheres to Python's 
best practices and follows PEP 8 style guidelines. Pylint checks for errors, potential issues,
and enforces consistent coding style, making it a valuable tool for maintaining code quality.

#### How to Install Pylint
To install Pylint, use the following command in your terminal:
```bash
pip install pylint
```

#### Running Pylint
Once installed, you can run Pylint on a specific Python file with:
```bash
pylint your_file.py
```
Or, to analyze all Python files in the project, run:
```bash
pylint speedtest_app/*.py
```
This setup is also configured to run automatically within GitHub Actions on every code push, 
checking the code with multiple Python versions for compatibility.
 
### Contribution
If you would like to contribute to the project, please create a fork of the repository and submit a Pull Request with your changes.

#### Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Create a new Pull Request

### Troubleshooting
If you encounter issues with the application, check the log file located in:
```
~/Documents/SpeedTest_Logs/speedtest_log.log
```

### Contact
For questions or suggestions, you can reach out to me via [GitHub](https://github.com/AlexTkDev).