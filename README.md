## Documentation for macOS_application_speedtest_for_python

### Project Description
`macOS_application_speedtest_for_python` is a macOS application designed to test your internet connection 
speed using Python. The program provides a convenient interface for measuring download, upload, and ping speeds, 
and also supports retesting and viewing test history.
The project is built based on another one of my applications, which you can check out on GitHub:
[Internet Speed Test](https://github.com/AlexTkDev/different_mini-apps/tree/main/check_internrt_speed)

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
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

### Usage
After installation, you can run the application by executing:
```bash
python alexs_speedtest.py
```

#### Features
- **Internet Speed Measurement**: The app allows you to test download and upload speeds, as well as ping (latency) of your internet connection.
- **Graphical Display**: After completing a test, users can view the test results and optionally plot the test history.
- **Repeat Test**: After a test is completed, users can repeat the test without needing to restart the application.
- **Test History**: The app saves the results of previous tests, allowing users to view the test history and visualize changes in speed.

#### Key Components
- **Tkinter**: Used for creating the graphical user interface (GUI), which includes buttons for starting tests, viewing results, and plotting graphs.
- **Speedtest-cli**: A library for performing internet speed tests, which powers the app's functionality.
- **Matplotlib**: A library for visualizing the test history by plotting graphs.
- **JSON**: A library for reading and writing test results stored in JSON format.

#### How It Works
1. When the app is launched, users can click the **"Start Speed Test"** button to initiate the test.
2. The app runs a speed test using the **speedtest-cli** library, measuring download speed, upload speed, and ping.
3. Once the test is completed, the results are displayed in the app's interface.
4. Users can save the test results to the **history.json** file and visualize the data using **matplotlib**.
5. For a repeat test, users can simply click the **"Repeat Speed Test"** button, which hides the history buttons until the new test is finished.


#### Building the Application
To build the application in `.app` format, run the following command:
```bash
pyinstaller main.spec
```
After building, the application will be located in the `dist` directory, and you can launch it by double-clicking the icon.

### Configuration
The project include a `alexs_speedtest.py` file, where you can find settings such as 
parameters for speed testing. Feel free to modify these parameters according to your needs.

### License
This project is licensed under the MIT License. Please refer to the `LICENSE` file for more detailed information.

### Code Analysis with Pylint
This project uses **Pylint** for static code analysis to ensure that code adheres to Python's 
best practices and follows PEP 8 style guidelines. Pylint checks for errors, potential issues,
and enforces consistent coding style, making it a valuable tool for maintaining code quality.

### How to Install Pylint
To install Pylint, use the following command in your terminal:
```bash
pip install pylint
```
### Running Pylint
Once installed, you can run Pylint on a specific Python file with:
```bash
pylint your_file.py
```
Or, to analyze all Python files in the project, run:
```bash
 pylint *.py
```
This setup is also configured to run automatically within GitHub Actions on every code push, 
checking the code with multiple Python versions for compatibility.
 
### Contribution
If you would like to contribute to the project, please create a fork of the repository and submit a Pull Request with your changes.

### Contact
For questions or suggestions, you can reach out to me via [GitHub](https://github.com/AlexTkDev).

