import unittest
from datetime import datetime
from queue import Queue

from src.exceptions import LineFormatError
from src.reader import Reader


class TestReader(unittest.TestCase):

    reader = Reader('unit-test', Queue())

    def test_parse_log_line(self):
        fixture_line = '199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245'
        formatted_line = {
            'remote_host': '199.72.81.55',
            'user_identity': '-',
            'user_name': '-',
            'datetime': datetime(1995, 6, 30, 20, 0, 1),
            'request': 'GET /history/apollo/ HTTP/1.0',
            'status_code': 200,
            'response_size': 6245,
            'section': '/history'
        }
        self.assertEqual(formatted_line, self.reader.parse_log_line(fixture_line))

        fixture_line = '199.72.81.55 - jeremy [01/Jul/1995:00:01:43 +0700] "GET / HTTP/1.0" 200 7074'
        formatted_line = {
            'remote_host': '199.72.81.55',
            'user_identity': '-',
            'user_name': 'jeremy',
            'datetime': datetime(1995, 7, 1, 7, 1, 43),
            'request': 'GET / HTTP/1.0',
            'status_code': 200,
            'response_size': 7074,
            'section': '/'
        }
        self.assertEqual(formatted_line, self.reader.parse_log_line(fixture_line))

        fixture_line = '199.72.81.55 [01/Jul/1995:00:01:43 +0700] "GET / HTTP/1.0" 200'
        self.assertRaises(LineFormatError, lambda: self.reader.parse_log_line(fixture_line))

    def test_get_section(self):
        self.assertEqual('/history', self.reader.get_section('GET /history/apollo/ HTTP/1.0'))
        self.assertEqual('/major-history', self.reader.get_section('GET /major-history/apollo/ HTTP/1.0'))
        self.assertEqual('/minor.history', self.reader.get_section('GET /minor.history/apollo/ HTTP/1.0'))
        self.assertEqual('/', self.reader.get_section('GET /history.php HTTP/1.0'))
        self.assertEqual('/', self.reader.get_section('GET / HTTP/1.0'))
        self.assertRaises(LineFormatError, lambda: self.reader.get_section('test test'))

    def test_parse_datetime(self):
        self.assertEqual(datetime(2006, 12, 7, 10, 23, 54), self.reader.parse_datetime('07/Dec/2006:14:23:54 -0400'))
        self.assertRaises(IndexError, lambda: self.reader.parse_datetime('07/Dec/2006:14:23:54'))
        self.assertRaises(ValueError, lambda: self.reader.parse_datetime('Test test'))

if __name__ == '__main__':
    unittest.main()
