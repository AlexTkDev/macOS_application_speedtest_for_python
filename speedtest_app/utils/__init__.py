"""
Utility functions for macOS_application_speedtest_for_python.
"""
import os
import platform
import json
import logging
from datetime import datetime

logger = logging.getLogger("SpeedTest")


def get_app_version():
    """Returns the current version of the application."""
    return "2.0.1"


def format_speed(speed_mbps):
    """Formats speed in Mbps to a readable string."""
    if speed_mbps >= 1000:
        return f"{speed_mbps / 1000:.2f} Gbps"
    return f"{speed_mbps:.2f} Mbps"


def get_user_data_dir():
    """Returns the path to the user data directory."""
    home = os.path.expanduser("~")
    if platform.system() == "Darwin":  # macOS
        return os.path.join(home, "Library", "Application Support", "AlexSpeedTest")
    elif platform.system() == "Windows":
        return os.path.join(home, "AppData", "Local", "AlexSpeedTest")
    else:
        return os.path.join(home, ".alexspeedtest")


def ensure_user_data_dir():
    """Creates the user data directory if it doesn't exist."""
    data_dir = get_user_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def save_settings(settings):
    """Saves application settings to a JSON file."""
    settings_file = os.path.join(ensure_user_data_dir(), "settings.json")
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        logger.info(f"Settings saved to {settings_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving settings: {e}", exc_info=True)
        return False


def load_settings():
    """Loads application settings from a JSON file."""
    settings_file = os.path.join(ensure_user_data_dir(), "settings.json")
    default_settings = {
        "auto_save_results": True,
        "show_network_info": True,
        "preferred_server_id": None,
        "dark_mode": False,
        "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if not os.path.exists(settings_file):
        return default_settings

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
            # Update with any missing default settings
            for key, value in default_settings.items():
                if key not in settings:
                    settings[key] = value
        logger.info(f"Settings loaded from {settings_file}")
        return settings
    except Exception as e:
        logger.error(f"Error loading settings: {e}", exc_info=True)
        return default_settings