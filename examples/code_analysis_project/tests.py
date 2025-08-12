import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestDataProcessing(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = [
            {'id': 1, 'name': 'Test Item 1', 'status': 'active'},
            {'id': 2, 'name': 'Test Item 2', 'status': 'inactive'}
        ]
    
    def test_process_data_valid_input(self):
        from main import process_data
        results = process_data(self.sample_data)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 1)
        self.assertEqual(results[0]['name'], 'Test Item 1')
    
    def test_process_data_empty_input(self):
        from main import process_data
        results = process_data([])
        
        self.assertEqual(results, [])
    
    @patch('main.requests.get')
    def test_fetch_data_success(self, mock_get):
        from main import fetch_data
        
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_data
        mock_get.return_value = mock_response
        
        result = fetch_data("https://api.example.com/data")
        self.assertEqual(result, self.sample_data)

if __name__ == '__main__':
    unittest.main()