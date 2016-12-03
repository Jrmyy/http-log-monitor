# -*- coding: utf-8 -*-

import re
import sys
from datetime import datetime, timedelta
from os import SEEK_END
from time import sleep
from queue import Queue

from src.custom_thread import ContinuousThread
from src.exceptions import LineFormatError


class Reader(ContinuousThread):
    """
       This thread is going to read each line of the access-log file, format the line into a dictionary and put the
       parsed line in a queue, shared with the displayer. It also put the date of each line in a second queue, shared
       with the alert system to keep track of traffic in the last alert_interval time (default is 2 minutes)

        Attributes
        ----------
        log_path: str
            path to the log file that will be read
        input_queue: Queue
            This queue is shared with the displayer and contains each line parsed into a dictionary
        input_traffic_queue: Queue
            This list contains only the date of each read line. It is shared with the alert system to count the number
            of requests of the last 2 minutes
        """

    def __init__(self, log_path, read_line_queue, traffic_queue):
        super().__init__()
        self.log_path = log_path
        self.input_queue = read_line_queue
        self.input_traffic_queue = traffic_queue

    def run(self):
        """
        First we are going to open the log file to read, throw an exception if we can't
        While the thread can run:
         - We go at the end of the file and we assume that there are lines after
         - We read each line and we repeat the process
         - Each read line is put in the input_queue and the date is put in the input_traffic_queue
        """

        # We are trying to open the file and to go the new added lines
        try:
            log_file = open(self.log_path)
        except IOError:
            print('Unable to open the file')
            sys.exit()

        # We go at the end of the file
        log_file.seek(0, SEEK_END)
        while self.can_run:
            end_of_file = False
            while not end_of_file:
                log_line = log_file.readline()
                if not log_line:
                    end_of_file = True
                    sleep(0.1)
                else:
                    try:
                        parsed_line = self.parse_log_line(log_line)
                        self.input_queue.put(parsed_line)
                        self.input_traffic_queue.put(parsed_line['datetime'])
                    except LineFormatError:
                        sys.exit()

    def parse_log_line(self, line):
        """
        We parse the line with several regex
        :param line:
        :return dict:
        """
        # We create the pattern and we inject the variable we want for the different parts
        pattern = re.compile(
            r'^(?P<remote_host>\S*) (?P<user_identity>\S*) (?P<user_name>\S*) \[(?P<datetime>.*?)\]'
            r' \"(?P<request>.*)\" (?P<status_code>\d*) (?P<response_size>\d*)$'
        )

        matching_pattern = pattern.match(line)

        # We raise an Exception if the line doesn't match the pattern
        if not matching_pattern:
            raise LineFormatError("The line doesn't match with the required format")

        # The formatted_line variable is a dictionary with the variable named before
        formatted_line = matching_pattern.groupdict()

        # We first cast the response size (in bytes) and the status code in int and we raise an Exception if we throw a
        # Value Error Exception
        try:
            formatted_line['response_size'] = int(formatted_line['response_size'])
            formatted_line['status_code'] = int(formatted_line['status_code'])
        except ValueError:
            raise LineFormatError("The status code or the response size aren't integers")

        formatted_line['section'] = self.get_section(formatted_line['request'])

        # Now we are going to format the date in the native datetime format
        try:
            formatted_line['datetime'] = self.parse_datetime(formatted_line['datetime'])
        except (ValueError, IndexError):
            raise LineFormatError("The date doesn't match with the required format")
        return formatted_line

    def get_section(self, request):
        """
        We get the section of each requested url
        For instance, the section of "/test/foo/bar" will be "/test"
        :param request:
        :return str:
        """
        section = re.match(r'^\S+ (/\S*) \S+', request.strip())

        # If the section doesn't match with the regex, we raise a LineFormatError
        if not section:
            raise LineFormatError("The request doesn't match with the expected output")

        # Then we handle the root case (if the request is for / or for /element.ext)
        section = section.group(1)
        if section.count('/') == 1:
            return '/'

        uri_parts = section.split("/")
        for part in uri_parts:
            if part != '':
                return '/' + str(part)

    def parse_datetime(self, string_datetime):
        """
        We transform the string datetime in a python datetime object (we pay attention to the timezone offset)
        :param string_datetime:
        :return datetime:
        """
        datetime_result = datetime.strptime(string_datetime[0:20], '%d/%b/%Y:%X')

        # The string date has the following format 01/Jul/1995:00:00:09 -0400 so so the basic date is 20 characters long
        # and the timezone is the 22th character, so at index 21
        if string_datetime[21] == '+':

            # The we just take the value of the timezone, that we divide by one hundred
            datetime_result -= timedelta(hours=int(string_datetime[22:26]) / 100)

        elif string_datetime[21] == '-':

            datetime_result += timedelta(hours=int(string_datetime[22:26]) / 100)

        return datetime_result
