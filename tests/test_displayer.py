import unittest
from queue import Queue
from datetime import datetime
from src.displayer import Displayer


class TestDisplayer(unittest.TestCase):

    displayer = Displayer(Queue(), {}, 1)

    def test_find_top_section(self):

        # Test with 3 hits on 2 pages
        formatted_line = {'section': '/history'}
        self.displayer.output_queue.put(formatted_line)
        formatted_line = {'section': '/'}
        self.displayer.output_queue.put(formatted_line)
        formatted_line = {'section': '/'}
        self.displayer.output_queue.put(formatted_line)

        top_section = self.displayer.find_top_section()

        self.assertEqual(top_section['hits'], 2)
        self.assertEqual(top_section['section'], '/')
        self.assertEqual(top_section['total_hits'], 3)
        self.assertEqual(top_section['percentage'], 67)
        self.assertEqual(top_section['display_interval'], 1)
        self.assertTrue('time' in top_section.keys())
        self.assertIsInstance(top_section['time'], datetime)

        # No traffic test response
        self.displayer.output_queue = Queue()
        top_empty_section = self.displayer.find_top_section()
        self.assertEqual(top_empty_section['display_interval'], 1)
        self.assertTrue('time' in top_empty_section.keys())
        self.assertIsInstance(top_empty_section['time'], datetime)


if __name__ == '__main__':
    unittest.main()
