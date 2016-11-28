# -*- coding: utf-8 -*-

from time import strftime, sleep
import sys
from queue import Queue, Empty
from src.lib.core.custom_thread import ContinuousThread


class Displayer(ContinuousThread):

    def __init__(self, queue: Queue, interval=10):
        super().__init__()
        self.sleep_time = interval
        self.queue = queue

    def run(self):
        while self.can_run:
            sleep(self.sleep_time)
            try:
                display_information = self.find_top_section()
                current_time = strftime('%H:%M:%S') + ' - '
                if display_information:
                    print(
                        current_time + 'Top section during the last 10 seconds is: ' + display_information['section'] +
                        '\n\tSection hits: ' + str(display_information['hits']) +
                        '\n\tPercentage of the whole traffic: ' +
                        str(round(int(display_information['hits']) / int(display_information['total_hits']) * 100)) +
                        '%\n\tTotal hits: ' + display_information['total_hits'])
                else:
                    print(current_time + 'No traffic on the website during the last 10 seconds')
            except Empty:
                sys.exit()

    def find_top_section(self):
        sections = {}
        while not self.queue.empty():
            parsed_line = self.queue.get()
            section = parsed_line['section']
            if section not in sections.keys():
                sections[section] = 1
            else:
                sections[section] += 1

        if sections != {}:
            max_section = max(sections, key=sections.get)
            return {
                'section': max_section,
                'hits': str(sections[max_section]),
                'total_hits': str(sum(sections.values()))
            }

        return None
