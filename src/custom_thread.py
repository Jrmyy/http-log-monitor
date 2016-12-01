from threading import Thread, Condition


class ContinuousThread(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.paused = True
        self.state = Condition()
        self.can_run = True

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()