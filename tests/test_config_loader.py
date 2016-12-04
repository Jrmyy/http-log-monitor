import unittest
import os
from src.config_loader import ConfigLoader


class MyTestCase(unittest.TestCase):

    DIR_NAME = os.path.dirname(os.path.abspath(__file__))

    config_loader = ConfigLoader(DIR_NAME + '/test_config.ini')

    def test_configure_threads(self):
        class_parameters = {
            'reader': {
                'log_path': '/path/to/test'
            },
            'displayer': {
                'display_interval': 99
            },
            'alert_system': {
                'max_requests_per_second': 14,
                'alert_interval': 112
            },
            'log_simulator': {
                'file_to_write': '/path/to/test/test',
                'hostname': 'ryuk',
                'sections': ['/', '/section1', '/section2']
            }
        }
        self.assertEqual(self.config_loader.configure_threads(), class_parameters)

    def test_configure_threads_no_sim(self):
        self.config_loader.config_file = self.DIR_NAME + '/test_config_no_sim.ini'
        class_parameters = {
            'reader': {
                'log_path': '/path/to/test'
            },
            'displayer': {
                'display_interval': 99
            },
            'alert_system': {
                'max_requests_per_second': 14,
                'alert_interval': 112
            },
            'log_simulator': None
        }
        self.assertEqual(self.config_loader.configure_threads(), class_parameters)


if __name__ == '__main__':
    unittest.main()
