import socket
import platform
import logging
import psutil
from datetime import datetime

# Получаем логгер
logger = logging.getLogger("SpeedTest")


def get_network_info():
    """
    Fetches network information including computer name, IP and MAC addresses.

    Returns:
        dict: Dictionary containing computer name and network adapter information

    Raises:
        Exception: If there's an error retrieving network information
    """
    try:
        # Initialize network information dictionary
        network_info = {
            "Computer Name": platform.node(),  # Get the computer's hostname
            "System": f"{platform.system()} {platform.release()}",
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Adapters": []  # List to store network adapters' info
        }

        logger.info(f"Getting network info for {network_info['Computer Name']}")

        # Get network stats
        net_stats = psutil.net_io_counters(pernic=True)

        # Loop through network interfaces and their addresses
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            adapter_info = {
                "Adapter": interface_name,
                "IP Address": None,
                "MAC Address": None,
                "IPv6 Address": None,
                "Netmask": None,
                "Active": False,
                "Bytes Sent": 0,
                "Bytes Received": 0
            }

            # Check if adapter is active (has network stats)
            if interface_name in net_stats:
                adapter_info["Active"] = True
                adapter_info["Bytes Sent"] = net_stats[interface_name].bytes_sent
                adapter_info["Bytes Received"] = net_stats[interface_name].bytes_recv

            # Get MAC and IP addresses for each adapter
            for address in interface_addresses:
                if address.family == socket.AF_LINK:
                    adapter_info["MAC Address"] = address.address
                elif address.family == socket.AF_INET:
                    adapter_info["IP Address"] = address.address
                    adapter_info["Netmask"] = address.netmask
                elif address.family == socket.AF_INET6:
                    adapter_info["IPv6 Address"] = address.address

            # Add adapter info if both IP and MAC addresses are found
            if adapter_info["IP Address"] and adapter_info["MAC Address"]:
                network_info["Adapters"].append(adapter_info)
                logger.debug(
                    f"Found adapter: {interface_name} with IP: {adapter_info['IP Address']}")

        if not network_info["Adapters"]:
            logger.warning("No network adapters with both IP and MAC addresses found")

        return network_info

    except Exception as e:
        logger.error(f"Error retrieving network information: {e}", exc_info=True)
        # Return basic info with error message
        return {
            "Computer Name": platform.node(),
            "System": f"{platform.system()} {platform.release()}",
            "Error": str(e),
            "Adapters": []
        }


def get_active_adapter_info():
    """Возвращает информацию о текущем активном сетевом адаптере."""
    try:
        all_info = get_network_info()
        active_adapters = [adapter for adapter in all_info["Adapters"]
                         if adapter["Active"] and adapter["IP Address"]]

        if not active_adapters:
            logger.warning("No active network adapters found")
            return None

        # Сортировка по объему принятых данных
        active_adapters.sort(key=lambda x: x["Bytes Received"], reverse=True)
        return active_adapters[0]

    except Exception as e:
        logger.error(f"Error getting active adapter info: {e}", exc_info=True)
        return None