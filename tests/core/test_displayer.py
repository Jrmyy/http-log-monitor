import unittest
from queue import Queue
from src.lib.core.displayer import Displayer


class TestDisplayer(unittest.TestCase):

    displayer = Displayer(Queue(), 1)
    display_information = {
        'section': '/',
        'hits': '2',
        'total_hits': '3'
    }

    def test_find_top_section(self):
        formatted_line = {'section': '/history'}
        self.displayer.queue.put(formatted_line)
        formatted_line = {'section': '/'}
        self.displayer.queue.put(formatted_line)
        formatted_line = {'section': '/'}
        self.displayer.queue.put(formatted_line)
        self.assertEqual(self.display_information, self.displayer.find_top_section())

        self.displayer.queue = Queue()
        self.assertIsNone(self.displayer.find_top_section())


if __name__ == '__main__':
    unittest.main()
