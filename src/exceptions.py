

class LineFormatError(Exception):
    pass


class ConfigError(Exception):

    def __init__(self, message):
        self.message = message