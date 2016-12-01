from time import sleep, strftime
from src.custom_thread import ContinuousThread
from src.alert_system import AlertSystem


class AlertDisplayer(ContinuousThread):

    def __init__(self, alert_content: dict):
        super().__init__()
        self.alert_content = alert_content

    def run(self):
        while self.can_run:
            if self.alert_content['to_display']:
                if self.alert_content['type'] == AlertSystem.ALERT_RAISE_TYPE:
                    print('High traffic generated an alert - hits = '+ str(self.alert_content['hits']) +
                          ' on the past 2 minutes, triggered at ' + str(self.alert_content['time']))
                elif self.alert_content['type'] == AlertSystem.ALERT_RECOVER_TYPE:
                    print('Alert recovery at ' + str(self.alert_content['time']))
                self.alert_content['to_display'] = False

