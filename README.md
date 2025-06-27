## 🚀 Internet Speed Test for macOS

A modern, beautiful, and fast macOS app to check your internet speed! Powered by Python, with a dark UI, smooth animations, and instant results. 

---

### ✨ Features
- ⚡ **One-click Speed Test** — Check your download, upload, and ping in seconds
- 🌙 **Modern Dark UI** — Stylish, easy on the eyes (ttkbootstrap)
- 🔔 **Toast Notifications** — Instant feedback for test results and errors
- 📊 **History & Graphs** — View, export, and plot your speed test history
- 🖥️ **Network Info** — See your active network adapter details
- 📝 **Logging** — All actions are logged for easy troubleshooting
- 🧪 **Fully Tested** — 100% passing unit tests, CI-ready

---

### 🛠️ Installation
**Requirements:**
- macOS 10.14+
- Python 3.8+ (with Tkinter)

```bash
# Clone the repo
git clone https://github.com/AlexTkDev/macOS_application_speedtest_for_python.git
cd macOS_application_speedtest_for_python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### ▶️ Usage
Run the app:
```bash
python main.py
```
Or build a native `.app`:
```bash
pyinstaller main.spec
open dist/Alex_SpeedTest.app
```

---

### 🧩 Project Structure
```
macOS_application_speedtest_for_python/
├── speedtest_app/         # Main package
│   ├── alexs_speedtest.py # Main app (async, threads)
│   ├── network_adapter_information.py
│   ├── test_history.py
│   ├── gui/
│   ├── utils/
│   └── tests/
├── main.py                # Entry point
├── main.spec              # PyInstaller config
├── requirements.txt       # Dependencies
├── setup.py               # Installer
├── README.md              # Docs
```

---

### 💡 How It Works
1. Click **Start Speed Test** — everything runs in the background, UI stays responsive
2. See your results instantly, repeat as needed
3. View/export your test history, plot interactive graphs
4. All network info and history are fetched asynchronously
5. Toasts notify you of completion or errors

---

### 🐞 Troubleshooting
- App won't open? Try:
  ```bash
  xattr -dr com.apple.quarantine dist/Alex_SpeedTest.app
  dist/Alex_SpeedTest.app/Contents/MacOS/alexs_speedtest
  ```
- Missing Tkinter? Reinstall Python with Tk support
- More help: check `~/Documents/SpeedTest_Logs/speedtest_log.log`

---

### 🧪 Tests
```bash
python -m unittest discover
```

---

### 📄 License
MIT — see `LICENSE`

---

### 🤝 Contributing
PRs welcome! See CONTRIBUTING in the repo.

---

### 💬 Contact
Questions or ideas? [Open an issue or reach out on GitHub](https://github.com/AlexTkDev)