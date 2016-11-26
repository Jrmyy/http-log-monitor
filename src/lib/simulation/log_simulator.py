from random import choice, randint
from string import ascii_lowercase
from datetime import datetime


class LogSimulator:

    def __init__(self, file_to_write):
        self.file_to_write = file_to_write
        self.requests = ['GET', 'PUT', 'POST', 'HEAD', 'DELETE', 'CONNECT', 'TRACE', 'OPTIONS']
        self.response_status = [200, 400, 500]
        self.hostname = 'localhost'
        self.last_date = datetime.now()
        self.sections = ['/', '/section1', '/section2', '/section3']

    def generate_log_line(self):
        return self.hostname + ' ' \
               + self.generate_random_word(6) + ' ' \
               + self.generate_random_word(6) + ' ' \
               + '[' + self.generate_random_date() + '] ' + ' ' \
               + '"' + self.generate_random_request() + ' ' \
               + self.generate_request_target() + ' ' \
               + 'HTTP/1.0"' + ' ' \
               + self.generate_random_response_status() + ' ' \
               + self.generate_random_bytes()

    def generate_random_word(self, length):
        return ''.join(choice(ascii_lowercase) for i in range(length))

    def generate_random_request(self):
        return choice(self.requests)

    def generate_random_response_status(self):
        return choice(self.response_status)

    def generate_random_bytes(self):
        return randint(100, 1000000)

    def generate_random_sub_domain(self):
        depth = randint(0, 4)
        sub_domain = '/'
        for i in range(depth):
            sub_domain += self.generate_random_word(randint(0, 10))

        sub_domain += self.generate_random_extension()
        return sub_domain

    def generate_request_target(self):
        return choice(self.sections) + self.generate_random_sub_domain()

    def generate_random_extension(self):
        return choice(['.php', '.html', ''])

    def generate_random_date(self):
        return ''
