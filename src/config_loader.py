from configparser import ConfigParser
from queue import Queue
from src.displayer import Displayer
from src.reader import Reader
from src.alert_system import AlertSystem
from src.log_simulator import LogSimulator
from src.exceptions import ConfigError


class ConfigLoader(ConfigParser):

    # expected_sections to be sure that there is no missing parameters and no useless section in the config file
    EXPECTED_SECTIONS = ['alert_system', 'displayer', 'log_simulator', 'reader']

    def __init__(self, config_file, use_simulator):
        super().__init__()
        self.config_file = config_file
        self.use_simulator = use_simulator

    # We configure the threads with the config file
    def configure_threads(self):
        self.read(self.config_file)
        sections = map(lambda x: x.lower(), self.sections())
        if sorted(sections) != ConfigLoader.EXPECTED_SECTIONS:
            raise ConfigError('The config format doesn\'t match with the wanted format')

        # Shared python objects
        #   - the read_line_queue, shared between the reader and the displayer
        #   - the total_traffic_hits_queue, shared between the alert system and the reader
        #   - the alert_contenct dictionary, shared between the alert system and the alert displayer


        read_line_queue = Queue()
        total_traffic_hits_queue = Queue()
        alert_content = {'type': AlertSystem.ALERT_RECOVER_TYPE, 'to_display': False}

        shared_parameters = {
            'log_simulator': {},
            'reader': {

            }

        }

        threads = {}

        for section in sections:
            lower_section = section.lower()
            threads[lower_section] = getattr(
                self,
                'self.provide_'+lower_section+'_class'
            )(
                class_parameters=self.items(section),
                shared_parameters=shared_parameters[lower_section]
            )

        return threads


    def provide_log_simulator_class(self, class_parameters, shared_parameters):
        print('totot')

    def provide_reader_class(self, class_parameters, shared_parameters):
        print('totot')

    def camel_case(self, string):
        names = string.split('_')
        names = map(lambda x: x.capitalize(), names)
        return ''.join(names)


