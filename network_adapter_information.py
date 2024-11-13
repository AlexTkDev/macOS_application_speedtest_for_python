import socket
import platform
import psutil


def get_network_info():
    """Fetches network information including computer name, IP and MAC addresses."""
    # Initialize network information dictionary
    network_info = {
        "Computer Name": platform.node(),  # Get the computer's hostname
        "Adapters": []  # List to store network adapters' info
    }

    # Loop through network interfaces and their addresses
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        adapter_info = {
            "Adapter": interface_name,
            "IP Address": None,
            "MAC Address": None
        }

        # Get MAC and IP addresses for each adapter
        for address in interface_addresses:
            if address.family == socket.AF_LINK:
                adapter_info["MAC Address"] = address.address
            elif address.family == socket.AF_INET:
                adapter_info["IP Address"] = address.address

        # Add adapter info if both IP and MAC addresses are found
        if adapter_info["IP Address"] and adapter_info["MAC Address"]:
            network_info["Adapters"].append(adapter_info)

    return network_info
