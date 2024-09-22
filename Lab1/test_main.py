import unittest
from unittest.mock import patch
import os
from main import main

class TestMainProgram(unittest.TestCase):
    @patch('builtins.input', side_effect=[
        '0.5',   # x input
        '0.001', # e input
        'Кінець', # End the program
        'No'     # Do not save results
    ])
    def test_main_no_save(self, mock_input):
        """Test main function when user chooses not to save results."""
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call('Data not saved to file')

    @patch('builtins.input', side_effect=[
        '0.5',   # x input
        '0.001', # e input
        'Кінець', # End the program
        'Yes',    # Save results
        'test1',  # Filename
    ])
    def test_main_save_new_file(self, mock_input):
        """Test main function when user saves results to a new file."""
        filename = 'test1'
        try:
            # Remove file if it exists
            if os.path.exists(filename):
                os.remove(filename)
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_any_call(f"Data saved to file '{filename}'. Total number of entries: 1")
        finally:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == '__main__':
    unittest.main()
