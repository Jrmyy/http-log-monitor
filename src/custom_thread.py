from threading import Thread, Condition


class ContinuousThread(Thread):
    """
    Custom thread, subclass of the python Thread, to make to program run forever

    Attributes
    ----------
    daemon: bool
        Decides if the thread has be to run as daemon
    paused: bool
        True if the thread is paused
    state: Condition
    can_run: bool
    """
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.paused = True
        self.state = Condition()
        self.can_run = True

    def resume(self):
        """
        Function to keep the thread running indefinitely
        """
        with self.state:
            self.paused = False
            self.state.notify()

    def stop(self):
        """
        Stop a thread
        """
        self.alive = False
        self.can_run = False