import unittest
from unittest.mock import patch
from app import app, index

class TestMonitoringApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('app.psutil.cpu_percent')
    @patch('app.psutil.virtual_memory')
    def test_index(self, mock_virtual_memory, mock_cpu_percent):
        # Set up mocked values
        mock_cpu_percent.return_value = 90
        mock_virtual_memory.return_value.percent = 85

        # Call the index route
        response = self.app.get('/')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'WARNING! High CPU or Memory Utilization detected. Please scale up.', response.data)
        self.assertIn(b'CPU Utilization: 90.0', response.data)
        self.assertIn(b'Memory Utilization: 85.0', response.data)

    @patch('app.psutil.cpu_percent')
    @patch('app.psutil.virtual_memory')
    def test_index_normal_utilization(self, mock_virtual_memory, mock_cpu_percent):
        # Set up mocked values
        mock_cpu_percent.return_value = 50
        mock_virtual_memory.return_value.percent = 60

        # Call the index route
        response = self.app.get('/')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'WARNING! High CPU or Memory Utilization detected. Please scale up.', response.data)
        self.assertIn(b'CPU Utilization: 50.0', response.data)
        self.assertIn(b'Memory Utilization: 60.0', response.data)

if __name__ == '__main__':
    unittest.main()