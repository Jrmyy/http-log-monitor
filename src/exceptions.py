class LineFormatError(Exception):
    """Exception raised when the line in the log file is not W3C-formatted"""
    pass


class ConfigError(Exception):
    """Exception raised when the config file contains error"""
    def __init__(self, message):
        self.message = message
