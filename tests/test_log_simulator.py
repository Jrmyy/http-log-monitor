import re
import unittest
from src.log_simulator import LogSimulator


class TestLogSimulator(unittest.TestCase):

    log_simulator = LogSimulator('unit-test', 'localhost', ['/', '/section1'])

    # Test that the generated word has the right length and is only lowercase letters
    def test_generate_word(self):
        generated_word = self.log_simulator.generate_word(6)
        self.assertEqual(len(generated_word), 6)
        self.assertTrue(generated_word.isalpha())
        self.assertTrue(generated_word.islower())

    # Test that the request type in one of the required
    def test_generate_request_type(self):
        self.assertIn(self.log_simulator.generate_request_type(), ['GET', 'PUT', 'POST', 'HEAD', 'OPTIONS'])

    # Test that the response status in one of the required
    def test_generate_response_status(self):
        self.assertIn(self.log_simulator.generate_response_status(), ['200', '400', '500'])

    # Test that the generated response size is a string containing only digits, and that its int value is between 100
    # and 10 000
    def test_generate_response_bytes(self):
        generated_bytes = self.log_simulator.generate_response_bytes()
        self.assertTrue(isinstance(generated_bytes, str))
        self.assertTrue(generated_bytes.isdigit())
        bytes_size = int(generated_bytes)
        self.assertTrue(bytes_size >= 100)
        self.assertTrue(bytes_size <= 10000)

    # Test that the request target has the right format
    def test_generate_request_target(self):
        self.assertTrue(re.match(r'/\S*', self.log_simulator.generate_request_target()))

    # Test that the sub section has the right format
    def test_generate_sub_section(self):
        self.assertTrue(re.match(r'/\S*', self.log_simulator.generate_sub_section()))

    # Test that the extension in one of the required
    def test_generate_extension(self):
        self.assertIn(self.log_simulator.generate_extension(), ['.php', '.html', ''])

    # Test that the generated datetime match the required format
    def test_generate_datetime(self):
        self.assertTrue(re.match(
            r'\d{2}/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}',
            self.log_simulator.generate_datetime()
        ))

    # Test that the generated log line match the regex used in the reader
    def test_generate_log_line(self):
        pattern = re.compile(r'^\S* \S* \S* \[.*?\] \".*\" \d* \d*$')
        self.assertTrue(pattern.match(self.log_simulator.generate_log_line()))

if __name__ == '__main__':
    unittest.main()
