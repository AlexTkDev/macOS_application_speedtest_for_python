"""
macOS_application_speedtest_for_python package.

A macOS application to test internet connection speed.
"""

__version__ = '2.0.1'
__author__ = 'Aleksandr'

from .network_adapter_information import get_network_info, get_active_adapter_info
from .test_history import save_test_results, view_history, plot_history

# speedtest_app/gui/__init__.py
"""
GUI components for macOS_application_speedtest_for_python.
"""

# speedtest_app/utils/__init__.py
"""
Utility functions for macOS_application_speedtest_for_python.
"""

# speedtest_app/tests/__init__.py
"""
Test modules for macOS_application_speedtest_for_python.
"""

# main.py
#!/usr/bin/env python3
"""
Entry point for macOS_application_speedtest application.
"""
import os
import sys

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from speedtest_app.alexs_speedtest import main

if __name__ == "__main__":
    main()