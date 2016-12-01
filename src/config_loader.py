from src.exceptions import ConfigError
from configparser import ConfigParser
from src.stats_displayer import StatisticalDisplayer
from src.reader import Reader
from src.alert_system import AlertSystem
from src.log_simulator import LogSimulator

class ConfigLoader(ConfigParser):

    expected_sections = ['alert_system', 'displayer', 'log_simulator', 'reader']

    def __init__(self, config_file: str):
        super().__init__()
        self.config_file = config_file

    def configure_threads(self):
        self.read(self.config_file)
        sections = self.sections()
        if sorted(map(lambda x: x.lower(), sections)) != self.expected_sections:
            raise ConfigError('The config format doesn\'t match with the wanted format')

        threads = {}

        for section in sections:
            section_parameters = dict(self.items(section))
            section = section.lower()
            class_name = self.camel_case(section)
            try:
                module = __import__('src.' + section)
                class_instance = getattr(module, class_name)
                instance = class_instance(**section_parameters)
                threads[section] = instance
            except (TypeError, ValueError):
                raise ConfigError('Impossible to instantiate the ' + class_name + ' thread')

        return threads

    def camel_case(self, string):
        names = string.split('_')
        names = map(lambda x: x.capitalize(), names)
        return ''.join(names)


