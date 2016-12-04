from time import time
from datetime import datetime
from src.custom_thread import ContinuousThread


class AlertSystem(ContinuousThread):
    """
    This class has to calculate whether or not to display an alert raising or recovering message. In order to do
    that, the AlertSystem thread has to calculate if the total_traffic on the past 2 minutes, divided by the alert
    interval is higher or lower than the threshold, defined by the maximum allowed requests per second

    Attributes
    ----------
    max_requests_per_second: int
        The allowed maximum number of requests per second
    output_traffic_queue: float
        This queue is shared with the reader and contains the date of each line read by the reader in the past
        alert_interval
    traffic_hits_list: list
        This list contains the date in the queue. We use this list in order to keep track of the lines read in the last
        alert_interval
    alert_content: dict
        This dictionary is shared with the alert displayer and contains all the information that will be displayed in
        case of an alert (raising or recovering)
    alert_interval: int
        The interval (in seconds) of calculation (default is 2 minutes, 120 seconds)
    """

    ALERT_RAISE_TYPE = 'alert_raise'
    ALERT_RECOVER_TYPE = 'alert_recover'

    def __init__(self, max_requests_per_second, output_traffic_queue, alert_content, alert_interval):
        super().__init__()
        self.max_requests_per_second = max_requests_per_second
        self.output_traffic_queue = output_traffic_queue
        self.traffic_hits_list = []
        self.alert_content = alert_content
        self.alert_interval = alert_interval

    def run(self):
        """
        While the thread can run it:
            - refreshes the list by keeping the elements that are still in the alert_interval
            - calculates if an alert raising or recovering must be displayed
            - Get the elements from the reader in the output_traffic_queue and put it in the traffic_hits_list and then
            refreshed the list
        """

        self.processing_time = time()

        while self.can_run:

            self.refresh_requests_list()

            if self.should_raise_alert_recover() and self.alert_content['type'] != AlertSystem.ALERT_RECOVER_TYPE:
                self.prepare_alert_recover_message()
            if self.should_raise_alert() and self.alert_content['type'] != AlertSystem.ALERT_RAISE_TYPE:
                self.prepare_alert_raise_message()

            while not self.output_traffic_queue.empty():
                line = self.output_traffic_queue.get()
                self.traffic_hits_list.append(line)
                self.refresh_requests_list()

    def should_raise_alert(self):
        """
        Calculate if the number of traffic hits on the interval period is higher than the maximum allowed
        """
        return len(self.traffic_hits_list) / self.alert_interval > self.max_requests_per_second

    def should_raise_alert_recover(self):
        """
        Calculate if the number of traffic hits on the interval period is lower than the maximum allowed
        """
        return len(self.traffic_hits_list) / self.alert_interval <= self.max_requests_per_second

    def prepare_alert_raise_message(self):
        """
        Populate the alert_content with the alert raising message elements
        """
        self.alert_content['hits'] = len(self.traffic_hits_list)
        self.alert_content['type'] = AlertSystem.ALERT_RAISE_TYPE
        self.prepare_message()

    def prepare_alert_recover_message(self):
        """
        Populate the alert_content with the alert recovering message elements
        """
        self.alert_content['type'] = AlertSystem.ALERT_RECOVER_TYPE
        self.prepare_message()

    def prepare_message(self):
        """
        Populate the alert_content with the common elements of each message type
        """
        self.alert_content['to_display'] = True
        self.alert_content['time'] = datetime.now()
        self.alert_content['alert_interval'] = self.alert_interval

    def refresh_requests_list(self):
        """
        Refresh the traffic_hits_list by keeping only the elements that are closer enough of the current time. The
        elements are sorted by ascending time so we go in the list and if we met an element that is close of the current
        time, we don't need to go further in the list and we stop the algorithm
        """
        current_time = datetime.utcnow()
        for line in self.traffic_hits_list:
            if (current_time - line).total_seconds() > self.alert_interval:
                self.traffic_hits_list.remove(line)
            else:
                return
