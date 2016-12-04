# -*- coding: utf-8 -*-

from time import time
from datetime import datetime
from threading import Lock
from src.alert_system import AlertSystem
from src.custom_thread import ContinuousThread
from shutil import get_terminal_size
from queue import Queue


class Displayer(ContinuousThread):

    """
    This thread aims to display the stats and the alert. It will display the stats each display interval and display
    alert message when it has to

    Attributes
    ----------
    output_queue: Queue
        This queue is shared with the reader and contains all the read and parsed line of the log file in order to make
        the statistics
    alert_content: dict
        This dict contains all the necessary information in order to display the right alert message
    display_interval: int
        In seconds, it is the time between two prints of the statistics concerning the traffic
    console_lock: Lock
        This lock enables to print safely
    terminal_size: int
        Int to represent to size of the terminal in order to print center messages
    """

    # Style and weight ids
    BOLD_WEIGHT = 'bold'
    NONE_STYLE = 'none'
    ALERT_STYLE = 'alert'
    OK_STYLE = 'ok'

    # Style and weight tag to be put in string
    BOLD_TAG = '\033[1m'
    NONE_TAG = ''
    ALERT_TAG = '\033[91m'
    OK_TAG = '\033[92m'
    END_TAG = '\033[0m'

    def __init__(self, output_queue, alert_content, display_interval):
        super().__init__()
        self.output_queue = output_queue
        self.alert_content = alert_content
        self.display_interval = display_interval
        self.console_lock = Lock()
        self.terminal_size = get_terminal_size().columns

    def run(self):
        """
        We are going to print the welcome message and then print the stats each display_interval seconds and print the
        alert messages when we need to
        :return:
        """

        starting_message = '* Welcome to the HTTP Log monitoring system *'
        starting_message = '*' * len(starting_message) + '\n' + starting_message + '\n' + '*' * len(starting_message) \
                           + '\n' + 'Starting at ' + datetime.now().strftime('%X') + '\n'

        self.print_center(starting_message, Displayer.NONE_STYLE, Displayer.BOLD_WEIGHT)

        last_display_time = time()
        while self.can_run:

            # Stats displaying
            time_difference = time() - last_display_time
            if time_difference >= self.display_interval:
                display_information = self.find_top_section()
                if 'section' in display_information.keys():
                    stats_message = '{time:%X} - Top section during the last {display_interval} seconds is: {section}' \
                                    '\n\tSection hits: {hits} \n\tPercentage of the whole traffic: {percentage}%' \
                                    '\n\tTotal hits: {total_hits}'.format(**display_information)
                else:
                    stats_message = '{time:%X} - No traffic on the website on the last ' \
                                    '{display_interval} seconds'.format(**display_information)
                last_display_time = time()
                self.lock_print(stats_message)

            # Alert displaying
            if 'to_display' in self.alert_content and self.alert_content['to_display']:
                # Alert raising message formatting
                if self.alert_content['type'] == AlertSystem.ALERT_RAISE_TYPE:
                    alert_message = 'High traffic generated an alert - hits = {hits}' \
                          ' on the past {alert_interval} seconds, triggered at {time:%X}'.format(**self.alert_content)
                    style = Displayer.ALERT_STYLE
                # We are in the alert recovery case
                else:
                    alert_message = 'Alert recovery at {time:%X}'.format(**self.alert_content)
                    style = Displayer.OK_STYLE
                remaining_space = round((self.terminal_size - len(alert_message)) / 2 - 10)
                alert_message = '*' * remaining_space + ' ' + alert_message + ' ' + '*' * remaining_space
                self.print_center(alert_message, style, Displayer.BOLD_WEIGHT)
                # We set the message as displayed
                self.alert_content['to_display'] = False

    def find_top_section(self):
        """
        Find the top section and return the information to be displayed each display_interval
        :return display_information:
        """
        sections = {}

        while not self.output_queue.empty():
            parsed_line = self.output_queue.get()
            section = parsed_line['section']
            if section not in sections.keys():
                sections[section] = 1
            else:
                sections[section] += 1

        current_time = datetime.now()

        display_information = {
            'time': current_time,
            'display_interval': self.display_interval
        }

        if sections != {}:
            max_section = max(sections, key=sections.get)
            total_hits = sum(sections.values())
            section_hits = sections[max_section]
            display_information['section'] = max_section
            display_information['hits'] = section_hits
            display_information['percentage'] = round(section_hits/ total_hits * 100)
            display_information['total_hits'] = total_hits

        return display_information

    def lock_print(self, string, style=NONE_STYLE, weight=NONE_STYLE):
        """
        Thread-safe printing function with a certain style and a certain weight
        :param string:
        :param style:
        :param weight:
        :return:
        """
        with self.console_lock:
            print(
                getattr(self, weight.upper() + '_TAG') +
                getattr(self, style.upper() + '_TAG') +
                string +
                Displayer.END_TAG +
                Displayer.END_TAG
            )

    def print_center(self, string, style=NONE_STYLE, weight=NONE_STYLE):
        """
        Print at the center of the terminal
        :param string:
        :param style:
        :param weight:
        :return:
        """
        for line in string.split('\n'):
            self.lock_print(line.center(self.terminal_size), style, weight)
