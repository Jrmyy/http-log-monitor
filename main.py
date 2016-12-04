#!/usr/bin/python

import os
from src.config_loader import ConfigLoader

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    config = ConfigLoader(DIR_NAME + '/config.ini')
    threads = config.configure_threads()

    displayer = threads['displayer']
    reader = threads['reader']
    alert_system = threads['alert_system']

    has_simulator = False
    log_simulator = None

    if 'log_simulator' in threads.keys() and threads['log_simulator'] is not None:
        log_simulator = threads['log_simulator']
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
