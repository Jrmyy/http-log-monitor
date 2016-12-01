from src.custom_thread import ContinuousThread
from queue import Queue
from time import time, strftime
from datetime import datetime

class AlertSystem(ContinuousThread):

    ALERT_RAISE_TYPE = 'alert_raise'
    ALERT_RECOVER_TYPE = 'alert_recover'

    def __init__(self, threshold: int, total_traffic_hits_queue: Queue, alert_content: dict):
        super().__init__()
        self.max_request_per_second = threshold
        self.total_traffic_hits_queue = total_traffic_hits_queue
        self.total_traffic_hits = []
        self.alert_content = alert_content

    def run(self):

        while self.can_run:

            self.refresh_requests_list()

            if self.should_raise_alert_recover() and self.alert_content['type'] != AlertSystem.ALERT_RECOVER_TYPE:
                self.prepare_alert_recover_message()
            if self.should_raise_alert() and self.alert_content['type'] != AlertSystem.ALERT_RAISE_TYPE:
                self.prepare_alert_raise_message()

            while not self.total_traffic_hits_queue.empty():
                line = self.total_traffic_hits_queue.get()
                self.total_traffic_hits.append(line)
                self.refresh_requests_list()

    def should_raise_alert(self):
        return len(self.total_traffic_hits) / 120 > self.max_request_per_second

    def should_raise_alert_recover(self):
        return len(self.total_traffic_hits) / 120 <= self.max_request_per_second

    def prepare_alert_raise_message(self):
        self.alert_content['hits'] = len(self.total_traffic_hits)
        self.alert_content['type'] = AlertSystem.ALERT_RAISE_TYPE
        self.prepare_message()

    def prepare_alert_recover_message(self):
        self.alert_content['type'] = AlertSystem.ALERT_RECOVER_TYPE
        self.prepare_message()

    def prepare_message(self):
        self.alert_content['to_display'] = True
        self.alert_content['time'] = strftime('%H:%M:%S')

    def refresh_requests_list(self):
        current_time = datetime.utcnow()
        for line in self.total_traffic_hits:
            if (current_time - line).total_seconds() > 120:
                self.total_traffic_hits.remove(line)
            else:
                return


