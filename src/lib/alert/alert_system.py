from src.lib.core.custom_thread import ContinuousThread


class AlertSystem(ContinuousThread):

    def __init__(self, threshold):
        super().__init__()
        self.threshold = threshold

