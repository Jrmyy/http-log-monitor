import os
import sys

sys.path.append(os.getcwd())

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

from queue import Queue
from src.log_simulator import LogSimulator
from src.reader import Reader
from src.stats_displayer import StatisticalDisplayer
from src.alert_system import AlertSystem
from src.alert_displayer import AlertDisplayer

read_line_queue = Queue()
total_traffic_hits_queue = Queue()
alert_content = {'type' : AlertSystem.ALERT_RECOVER_TYPE, 'to_display': False}

reader = Reader('/Applications/AMPPS/apache/logs/access_log', read_line_queue, total_traffic_hits_queue)
stats_displayer = StatisticalDisplayer(read_line_queue)
alert_system = AlertSystem(1/120, total_traffic_hits_queue, alert_content)
alert_displayer = AlertDisplayer(alert_content)

reader.start()
stats_displayer.start()
alert_system.start()
alert_displayer.start()

while True:
    reader.resume()

    stats_displayer.resume()
    alert_system.resume()
    alert_displayer.resume()