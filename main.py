import sys
import os
sys.path.append(os.getcwd())

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

from src.lib.core.reader import Reader
from src.lib.core.displayer import Displayer
from src.lib.simulation.log_simulator import LogSimulator
from queue import Queue
from src.lib.core.user_input import UserInput

queue = Queue()

reader = Reader(DIR_NAME + '/data/access-log.log', queue)
log_simulator = LogSimulator(DIR_NAME + '/data/access-log.log', 100000)
displayer = Displayer(queue)

reader.start()
log_simulator.start()
displayer.start()

while True:
    reader.resume()
    log_simulator.resume()
    displayer.resume()



