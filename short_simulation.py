#!/usr/bin/python

import os
from src.displayer import Displayer
from src.reader import Reader
from src.alert_system import AlertSystem
from src.log_simulator import LogSimulator
from time import time
from queue import Queue

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    read_line_queue = Queue()
    traffic_queue = Queue()
    alert_content = {'type': AlertSystem.ALERT_RECOVER_TYPE, 'to_display': False}

    reader = Reader(DIR_NAME + '/data/access-log.log', read_line_queue, traffic_queue)
    displayer = Displayer(read_line_queue, alert_content, 10)
    alert_system = AlertSystem(80, traffic_queue, alert_content, 120)
    log_simulator = LogSimulator(DIR_NAME + '/data/access-log.log', 'localhost', ['/', '/section1'])

    current_time = time()

    log_simulator.start()
    reader.start()
    displayer.start()
    alert_system.start()

    while time() - current_time <= 120:
        log_simulator.resume()
        reader.resume()
        displayer.resume()
        alert_system.resume()

    current_time = time()
    log_simulator.stop()

    while time() - current_time <= 60:
        reader.resume()
        displayer.resume()
        alert_system.resume()