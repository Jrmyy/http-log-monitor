# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from random import choice, randint, uniform
from string import ascii_lowercase
from time import strftime, gmtime
from src.custom_thread import ContinuousThread
from _thread import interrupt_main


class LogSimulator(ContinuousThread):
    """
    This thread is used in case you don't have an apache web server on your computer. It will fill a file with
    log line correctly formatted.

    Attributes
    ----------
    file_to_write: str
        path to the log file that will be read
    requests: list
        the list of allowed requests type
    hostname: str
        the hostname monitored
    sections: list
        The different sections of the website
    """

    def __init__(self, file_to_write, hostname, sections):
        super().__init__()
        self.file_to_write = file_to_write
        self.requests = ['GET', 'PUT', 'POST', 'HEAD', 'OPTIONS']
        self.hostname = hostname
        self.sections = sections

    def run(self):
        """
        The thread is going to open the file in which it has to write
        Then while it can run it will generate random log line and put it in the log file
        :return:
        """
        try:
            log_file = open(self.file_to_write, 'w')
        except IOError:
            print('Unable to open the file for writing')
            interrupt_main()

        while self.can_run:
            lines_in_batch = 0
            try:
                log_file.write(self.generate_log_line())
                lines_in_batch += 1
                if lines_in_batch % 100 == 0:
                    log_file.flush()
            except BaseException:
                log_file.close()
                interrupt_main()

            log_file.flush()

        log_file.close()

    def generate_log_line(self):
        """
        Generate a random W3C-formatted log line
        :return:
        """
        return self.is_a_comment_line() \
               + self.hostname + ' ' \
               + self.generate_word(6) + ' ' \
               + self.generate_word(6) + ' ' \
               + '[' + self.generate_datetime() + ']' + ' ' \
               + '"' + self.generate_request_type() + ' ' \
               + self.generate_request_target() + ' ' \
               + 'HTTP/1.1"' + ' ' \
               + self.generate_response_status() + ' ' \
               + self.generate_response_bytes() + '\n'

    def is_a_comment_line(self):
        """
        Decide if a line should be commented or not and return # if the line is commented
        :return string:
        """
        random = uniform(0, 1)
        if random <= 0.01:
            return '#'
        return ''

    def generate_word(self, length):
        """
        Generate a random string of the wanted length
        :param length:
        :return:
        """
        return ''.join(choice(ascii_lowercase) for i in range(length))

    def generate_request_type(self):
        """
        Choose randomly a request type in the list
        :return:
        """
        return choice(self.requests)

    def generate_response_status(self):
        """
        Return a randomly chosen status code
        :return:
        """
        random = uniform(0, 1)
        if random < 0.1:
            return '400'

        if random > 0.9:
            return '500'

        return '200'

    def generate_response_bytes(self):
        """
        Return a random response size
        :return:
        """
        return str(randint(100, 10000))

    def generate_request_target(self):
        """
        Generate the request url
        :return str:
        """
        section = choice(self.sections)
        if section != '/':
            section += self.generate_sub_section()
        return section

    def generate_sub_section(self):
        """
        Return a random sub section by create random string on a random depth
        :return str:
        """
        depth = randint(0, 4)

        if depth == 0:
            return '/'

        sub_domain = ''
        for i in range(depth):
            sub_domain += '/' + self.generate_word(randint(3, 10))

        sub_domain += self.generate_extension()
        return sub_domain

    def generate_extension(self):
        """
        return random file extension
        :return:
        """
        return choice(['.php', '.html', ''])

    def generate_datetime(self):
        """
        Generate random string datetime
        :return str:
        """
        return datetime.now().strftime('%d/%b/%Y:%X') + ' ' + strftime("%z", gmtime())
