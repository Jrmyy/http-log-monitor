#!/usr/bin/python

import os
import sys
from src.config_loader import ConfigLoader
from queue import Queue
from src.log_simulator import LogSimulator
from src.reader import Reader
from src.displayer import Displayer
from src.alert_system import AlertSystem

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    try:

        config = ConfigLoader(DIR_NAME + '/config.ini')
        parameters = config.configure_threads()

        read_line_queue = Queue()
        traffic_queue = Queue()
        alert_content = {'type': AlertSystem.ALERT_RECOVER_TYPE, 'to_display': False}

        reader = Reader(input_queue=read_line_queue, input_traffic_queue=traffic_queue, **parameters['reader'])
        displayer = Displayer(output_queue=read_line_queue, alert_content= alert_content, **parameters['displayer'])
        alert_system = AlertSystem(
            output_traffic_queue=traffic_queue,
            alert_content=alert_content,
            **parameters['alert_system']
        )

        has_simulator = False
        log_simulator = None

        if 'log_simulator' in parameters.keys() and parameters['log_simulator'] is not None:
            log_simulator = LogSimulator(**parameters['log_simulator'])
            has_simulator = True

        displayer.start()
        reader.start()
        alert_system.start()

        if has_simulator:
            log_simulator.start()

        while True:
            displayer.resume()
            reader.resume()
            alert_system.resume()
            if has_simulator:
                log_simulator.resume()
    except KeyboardInterrupt:
        print('Shutting down the service ...')
        sys.exit(0)
