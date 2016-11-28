# -*- coding: utf-8 -*-

import sys
from random import choice, randint, uniform
from string import ascii_lowercase
from datetime import datetime
from time import strftime, gmtime, sleep
from src.lib.core.custom_thread import ContinuousThread


class LogSimulator(ContinuousThread):

    def __init__(self, file_to_write: str, request_per_second: int):
        super().__init__()
        self.file_to_write = file_to_write
        self.requests = ['GET', 'PUT', 'POST', 'HEAD', 'OPTIONS']
        self.hostname = 'localhost'
        self.sections = ['/', '/section1', '/section2', '/section3']
        self.requests_per_second = request_per_second

    def run(self):
        if self.requests_per_second != 0:
            try:
                log_file = open(self.file_to_write, 'w')
            except IOError:
                print('Unable to open the file for writting')
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

    def generate_log_line(self) -> str:
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

    def generate_word(self, length: int) -> str:
        return ''.join(choice(ascii_lowercase) for i in range(length))

    def generate_request_type(self) -> str:
        return choice(self.requests)

    def generate_response_status(self) -> str:
        random = uniform(0, 1)
        if random < 0.1:
            return '400'

        if random > 0.9:
            return '500'

        return '200'

    def generate_response_bytes(self) -> str:
        return str(randint(100, 10000))

    def generate_request_target(self) -> str:
        section = choice(self.sections)
        if section != '/':
            section += self.generate_sub_section()
        return section

    def generate_sub_section(self) -> str:
        depth = randint(0, 4)

        if depth == 0:
            return '/'

        sub_domain = ''
        for i in range(depth):
            sub_domain += '/' + self.generate_word(randint(3, 10))

        sub_domain += self.generate_extension()
        return sub_domain

    def generate_extension(self) -> str:
        return choice(['.php', '.html', ''])

    def generate_datetime(self) -> str:
        return datetime.now().strftime('%d/%b/%Y:%X') + ' ' + strftime("%z", gmtime())
