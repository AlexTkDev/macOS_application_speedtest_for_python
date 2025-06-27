# pylint: disable=too-many-instance-attributes,line-too-long,wrong-import-order,missing-final-newline,unused-import
import unittest
from unittest.mock import patch, MagicMock
import socket
from speedtest_app import network_adapter_information


class TestNetworkAdapter(unittest.TestCase):
    """Tests for the network_adapter_information module."""

    @patch('speedtest_app.network_adapter_information.platform')
    @patch('speedtest_app.network_adapter_information.psutil')
    def test_get_network_info_success(self, mock_psutil, mock_platform):
        """Test successful retrieval of network information."""
        # Setup mocks
        mock_platform.node.return_value = "TestComputer"
        mock_platform.system.return_value = "macOS"
        mock_platform.release.return_value = "12.0"

        # Mock network IO counters
        mock_net_io = {
            "en0": MagicMock(bytes_sent=1000, bytes_recv=2000),
            "lo0": MagicMock(bytes_sent=500, bytes_recv=500)
        }
        mock_psutil.net_io_counters.return_value = mock_net_io

        # Mock network interfaces
        mock_address_en0_ip = MagicMock(family=socket.AF_INET, address="192.168.1.10",
                                    netmask="255.255.255.0")
        mock_address_en0_mac = MagicMock(family=socket.AF_LINK, address="00:11:22:33:44:55")
        mock_address_en0_ipv6 = MagicMock(family=socket.AF_INET6, address="fe80::1")

        mock_address_lo0_ip = MagicMock(family=socket.AF_INET, address="127.0.0.1",
                                    netmask="255.0.0.0")
        mock_address_lo0_mac = MagicMock(family=socket.AF_LINK, address="00:00:00:00:00:00")

        mock_interfaces = {
            "en0": [mock_address_en0_ip, mock_address_en0_mac, mock_address_en0_ipv6],
            "lo0": [mock_address_lo0_ip, mock_address_lo0_mac]
        }
        mock_psutil.net_if_addrs.return_value = mock_interfaces

        # Call function
        result = network_adapter_information.get_network_info()

        # Assert results
        self.assertEqual(result["Computer Name"], "TestComputer")
        self.assertEqual(result["System"], "macOS 12.0")
        self.assertEqual(len(result["Adapters"]), 2)

        # Check en0 adapter
        en0_adapter = next((a for a in result["Adapters"] if a["Adapter"] == "en0"), None)
        self.assertIsNotNone(en0_adapter)
        if en0_adapter is not None:
            self.assertEqual(en0_adapter["IP Address"], "192.168.1.10")
            self.assertEqual(en0_adapter["MAC Address"], "00:11:22:33:44:55")
            self.assertEqual(en0_adapter["IPv6 Address"], "fe80::1")
            self.assertEqual(en0_adapter["Netmask"], "255.255.255.0")
            self.assertTrue(en0_adapter["Active"])
            self.assertEqual(en0_adapter["Bytes Sent"], 1000)
            self.assertEqual(en0_adapter["Bytes Received"], 2000)

    @patch('speedtest_app.network_adapter_information.platform')
    @patch('speedtest_app.network_adapter_information.psutil')
    def test_get_network_info_exception(self, mock_psutil, mock_platform):
        """Test handling of exceptions in get_network_info."""
        # Setup mocks to raise exception
        mock_platform.node.return_value = "TestComputer"
        mock_platform.system.return_value = "macOS"
        mock_platform.release.return_value = "12.0"
        mock_psutil.net_if_addrs.side_effect = Exception("Test exception")

        # Call function
        result = network_adapter_information.get_network_info()

        # Assert results
        self.assertEqual(result["Computer Name"], "TestComputer")
        self.assertEqual(result["System"], "macOS 12.0")
        self.assertEqual(len(result["Adapters"]), 0)
        self.assertIn("Error", result)
        self.assertEqual(result["Error"], "Test exception")

    @patch('speedtest_app.network_adapter_information.get_network_info')
    def test_get_active_adapter_info(self, mock_get_network_info):
        """Test retrieving active adapter info."""
        # Setup mock
        mock_get_network_info.return_value = {
            "Computer Name": "TestComputer",
            "System": "macOS 12.0",
            "Adapters": [
                {
                    "Adapter": "en0",
                    "IP Address": "192.168.1.10",
                    "MAC Address": "00:11:22:33:44:55",
                    "Active": True,
                    "Bytes Received": 5000,
                    "Bytes Sent": 1000
                },
                {
                    "Adapter": "en1",
                    "IP Address": "192.168.2.10",
                    "MAC Address": "AA:BB:CC:DD:EE:FF",
                    "Active": True,
                    "Bytes Received": 2000,
                    "Bytes Sent": 3000
                }
            ]
        }

        # Call function
        result = network_adapter_information.get_active_adapter_info()

        # Assert results - should return adapter with most bytes received
        self.assertIsNotNone(result)
        if result is not None:
            self.assertEqual(result["Adapter"], "en0")
            self.assertEqual(result["Bytes Received"], 5000)


if __name__ == '__main__':
    unittest.main()