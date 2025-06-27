"""
macOS_application_speedtest_for_python package.

A macOS application to test internet connection speed.
"""

__version__ = '3.0.0'
__author__ = 'Aleksandr'

from .network_adapter_information import get_network_info, get_active_adapter_info
from .test_history import save_test_results, view_history, plot_history

__all__ = [
    'get_network_info',
    'get_active_adapter_info',
    'save_test_results',
    'view_history',
    'plot_history'
]