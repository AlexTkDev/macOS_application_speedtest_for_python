import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from speedtest_app import test_history


class TestHistory(unittest.TestCase):
    """Tests for the test_history module."""

    def setUp(self):
        """Set up a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        self.history_path = os.path.join(self.test_dir, "test_history.json")

    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_dir)

    def test_save_test_results_new_file(self):
        """Test saving test results to a new file."""
        # Call function with test data
        test_history.save_test_results(
            100.5, 50.2, 20.1, self.history_path
        )

        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(self.history_path))

        with open(self.history_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["download_speed"], 100.5)
        self.assertEqual(data[0]["upload_speed"], 50.2)
        self.assertEqual(data[0]["ping"], 20.1)
        self.assertIn("timestamp", data[0])

    def test_save_test_results_existing_file(self):
        """Test appending test results to an existing file."""
        # Create initial file with data
        initial_data = [{"timestamp": "2024-04-01 12:00:00",
                         "download_speed": 80.0,
                         "upload_speed": 40.0,
                         "ping": 15.0}]

        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f)

        # Call function with new test data
        test_history.save_test_results(
            100.5, 50.2, 20.1, self.history_path
        )

        # Verify file contains both entries
        with open(self.history_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["download_speed"], 80.0)
        self.assertEqual(data[1]["download_speed"], 100.5)

    def test_save_test_results_invalid_json(self):
        """Test handling corrupted JSON file."""
        # Create a file with invalid JSON
        with open(self.history_path, 'w', encoding='utf-8') as f:
            f.write("This is not valid JSON")

        # Call function (should handle the error and create a new file)
        test_history.save_test_results(
            100.5, 50.2, 20.1, self.history_path
        )

        # Verify file contains valid data now
        with open(self.history_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["download_speed"], 100.5)

    @patch('test_history.messagebox')
    def test_view_history_no_file(self, mock_messagebox):
        """Test view_history when no history file exists."""
        root_mock = MagicMock()

        # Call function
        test_history.view_history(root_mock, self.history_path)

        # Verify messagebox was shown
        mock_messagebox.showinfo.assert_called_once_with("History", "No history available.")

    @patch('test_history.messagebox')
    def test_plot_history_no_file(self, mock_messagebox):
        """Test plot_history when no history file exists."""
        root_mock = MagicMock()

        # Call function
        test_history.plot_history(root_mock, self.history_path)

        # Verify messagebox was shown
        mock_messagebox.showinfo.assert_called_once_with("History", "No history available.")


if __name__ == '__main__':
    unittest.main()
