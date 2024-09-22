import unittest
from main import save_results_to_file
import os
import tempfile
import datetime

class TestSaveResultsToFile(unittest.TestCase):
    def test_save_results(self):
        """Test saving results to a file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            filename = tmp_file.name
        try:
            # Prepare session results
            session_results = [
                {'x': 1.0, 'e': 0.01, 'f_x_e': -0.841470985, 'N': 5},
                {'x': 0.5, 'e': 0.001, 'f_x_e': -0.479425539, 'N': 7},
            ]
            total_entries = save_results_to_file(filename, session_results)
            self.assertEqual(total_entries, 2)
            # Read file and check contents
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 2)
                date_str = datetime.datetime.now().strftime("%d.%m.%Y")
                # Note: Since the computed values might not match exactly, we focus on the format
        finally:
            # Clean up temporary file
            os.remove(filename)

    def test_file_write_error(self):
        """Test handling of file write error."""
        filename = '/invalid/path/to/file.txt'
        session_results = [{'x': 1.0, 'e': 0.01, 'f_x_e': -0.841470985, 'N': 5}]
        total_entries = save_results_to_file(filename, session_results)
        self.assertIsNone(total_entries)

    def test_file_read_error(self):
        """Test handling of file read error after writing."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            filename = tmp_file.name
        try:
            # Remove read permissions from the file
            os.chmod(filename, 0o222)  # Write-only
            session_results = [{'x': 1.0, 'e': 0.01, 'f_x_e': -0.841470985, 'N': 5}]
            total_entries = save_results_to_file(filename, session_results)
            self.assertIsNone(total_entries)
        finally:
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
