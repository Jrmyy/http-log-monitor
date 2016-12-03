# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from random import choice, randint, uniform
from string import ascii_lowercase
from time import strftime, gmtime

from src.custom_thread import ContinuousThread


class LogSimulator(ContinuousThread):

    def __init__(self, file_to_write):
        super().__init__()
        self.file_to_write = file_to_write
        self.requests = ['GET', 'PUT', 'POST', 'HEAD', 'OPTIONS']
        self.hostname = 'localhost'
        self.sections = ['/', '/section1', '/section2', '/section3']

    def run(self):
        try:
            log_file = open(self.file_to_write, 'w')
        except IOError:
            print('Unable to open the file for writing')
            sys.exit()

        while self.can_run:
            lines_in_batch = 0
            try:
                log_file.write(self.generate_log_line())
                lines_in_batch += 1
                if lines_in_batch % 100 == 0:
                    log_file.flush()
            except BaseException:
                sys.exit()

            log_file.flush()

        log_file.close()

    def generate_log_line(self):
        return self.is_a_comment_line() \
               + self.hostname + ' ' \
               + self.generate_word(6) + ' ' \
               + self.generate_word(6) + ' ' \
               + '[' + self.generate_datetime() + ']' + ' ' \
               + '"' + self.generate_request_type() + ' ' \
               + self.generate_request_target() + ' ' \
               + 'HTTP/1.0"' + ' ' \
               + self.generate_response_status() + ' ' \
               + self.generate_response_bytes() + '\n'

    def is_a_comment_line(self):
        random = uniform(0, 1)
        if random <= 0.01:
            return '#'
        return ''

    def generate_word(self, length):
        return ''.join(choice(ascii_lowercase) for i in range(length))

    def generate_request_type(self):
        return choice(self.requests)

    def generate_response_status(self):
        random = uniform(0, 1)
        if random < 0.1:
            return '400'

        if random > 0.9:
            return '500'

        return '200'

    def generate_response_bytes(self):
        return str(randint(100, 10000))

    def generate_request_target(self):
        section = choice(self.sections)
        if section != '/':
            section += self.generate_sub_section()
        return section

    def generate_sub_section(self):
        depth = randint(0, 4)

        if depth == 0:
            return '/'

        sub_domain = ''
        for i in range(depth):
            sub_domain += '/' + self.generate_word(randint(3, 10))

        sub_domain += self.generate_extension()
        return sub_domain

    def generate_extension(self):
        return choice(['.php', '.html', ''])

    def generate_datetime(self):
        return datetime.now().strftime('%d/%b/%Y:%X') + ' ' + strftime("%z", gmtime())
