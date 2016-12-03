#!/usr/bin/python

import os
from queue import Queue
from datetime import datetime
from src.log_simulator import LogSimulator
from src.reader import Reader
from src.displayer import Displayer
from src.alert_system import AlertSystem

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    read_line_queue = Queue()
    total_traffic_hits_queue = Queue()
    alert_content = {'type' : AlertSystem.ALERT_RECOVER_TYPE, 'to_display': False, 'time': datetime.now()}

    #reader = Reader('/Applications/AMPPS/apache/logs/access_log', read_line_queue, total_traffic_hits_queue)
    reader = Reader(DIR_NAME + '/data/access-log.log', read_line_queue, total_traffic_hits_queue)
    displayer = Displayer(read_line_queue, alert_content)
    log_simulator = LogSimulator(DIR_NAME + '/data/access-log.log')
    alert = AlertSystem(10, total_traffic_hits_queue, alert_content)

    displayer.start()
    log_simulator.start()
    reader.start()
    alert.start()

    while True:
        displayer.resume()
        log_simulator.resume()
        reader.resume()
        alert.resume()

