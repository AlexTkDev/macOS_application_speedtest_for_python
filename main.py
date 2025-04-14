#!/usr/bin/env python3
"""
Entry point for macOS_application_speedtest application.
"""
import sys
import os

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the main function from the package
from speedtest_app.alexs_speedtest import main

if __name__ == "__main__":
    main()