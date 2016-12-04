from configparser import ConfigParser
from queue import Queue
from src.displayer import Displayer
from src.reader import Reader
from src.alert_system import AlertSystem
from src.log_simulator import LogSimulator
from src.exceptions import ConfigError
from voluptuous import Required, All, Length, Range, Schema, MultipleInvalid
from distutils.util import strtobool
import sys


class ConfigLoader(ConfigParser):

    # expected_sections to be sure that there is no missing parameters and no useless section in the config file
    EXPECTED_SECTIONS = ['alert_system', 'displayer', 'log_simulator', 'reader']

    # Validation schema
    LOG_SIMULATOR_SCHEMA = Schema({
        Required('file_to_write'): All(str, Length(min=1)),
        Required('hostname'): All(str, Length(min=1)),
        Required('sections'): All(list, Length(min=1)),
        Required('enabled'): All(bool)
    })

    READER_SCHEMA = Schema({
        Required('log_path'): All(str, Length(min=1)),
        Required('input_queue'): All(Queue),
        Required('input_traffic_queue'): All(Queue)
    })

    DISPLAYER_SCHEMA = Schema({
        Required('display_interval'): All(int, Range(min=1)),
        Required('output_queue'): All(Queue),
        Required('alert_content'): All(dict)
    })

    ALERT_SYSTEM_SCHEMA = Schema({
        Required('max_requests_per_second'): All(int, Range(min=1)),
        Required('alert_interval'): All(int, Range(min=1)),
        Required('output_traffic_queue'): All(Queue),
        Required('alert_content'): All(dict)
    })

    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file

    # We configure the threads with the config file
    def configure_threads(self):
        self.read(self.config_file)
        lower_sections = [x.lower() for x in self.sections()]
        if sorted(lower_sections) != ConfigLoader.EXPECTED_SECTIONS:
            raise ConfigError('The config format doesn\'t match with the wanted format')

        # Shared python objects
        #   - the read_line_queue, shared between the reader and the displayer
        #   - the total_traffic_hits_queue, shared between the alert system and the reader
        #   - the alert_contenct dictionary, shared between the alert system and the alert displayer

        read_line_queue = Queue()
        traffic_queue = Queue()
        alert_content = {'type': AlertSystem.ALERT_RECOVER_TYPE, 'to_display': False}

        # We map the different threads with the shared elements they require
        shared_parameters = {
            'log_simulator': {},
            'reader': {
                'input_queue': read_line_queue,
                'input_traffic_queue': traffic_queue
            },
            'displayer': {
                'output_queue': read_line_queue,
                'alert_content': alert_content
            },
            'alert_system': {
                'output_traffic_queue': traffic_queue,
                'alert_content': alert_content
            }
        }

        threads = {}

        # We put each thread in a dictionary by calling the according providing method of each thread
        for section in self.sections():
            lower_section = section.lower()
            threads[lower_section] = getattr(
                self,
                'provide_'+lower_section+'_class'
            )(
                {**dict(self.items(section)), **shared_parameters[lower_section]}
            )

        return threads

    def provide_log_simulator_class(self, class_parameters):
        try:
            class_parameters['number_of_sections'] = int(class_parameters['number_of_sections'])
            class_parameters['enabled'] = bool(strtobool(class_parameters['enabled']))
        except (ValueError, KeyError):
            raise ConfigError('One of the parameter of the Log Simulator section doesn\'t match with the required type')

        if not class_parameters['enabled']:
            return None

        website_sections = ['/']
        if class_parameters['number_of_sections'] > 1:
            for i in range(1, class_parameters['number_of_sections']):
                website_sections.append('/section' + i)

        class_parameters['sections'] = website_sections
        del class_parameters['number_of_sections']

        self.validate_section('log_simulator', class_parameters)
        return LogSimulator(**class_parameters)

    def provide_reader_class(self, class_parameters):
        self.validate_section('reader', class_parameters)
        return Reader(**class_parameters)

    def provide_displayer_class(self, class_parameters):
        try:
            class_parameters['display_interval'] = int(class_parameters['display_interval'])
        except (KeyError, ValueError):
            raise ConfigError('The display interval of the Displayer must be integer')

        self.validate_section('displayer', class_parameters)
        return Displayer(**class_parameters)

    def provide_alert_system_class(self, class_parameters):
        try:
            class_parameters['max_requests_per_second'] = int(class_parameters['max_requests_per_second'])
            class_parameters['alert_interval'] = int(class_parameters['alert_interval'])
        except (KeyError, ValueError):
            raise ConfigError('The maximum number of requests per second and the alert interval of the alert system '
                              'must be integers')

        self.validate_section('alert_system', class_parameters)
        return AlertSystem(**class_parameters)

    def validate_section(self, thread_name, class_parameters):
        try:
            getattr(self, thread_name.upper() + '_SCHEMA')(class_parameters)
        except MultipleInvalid as e:
            raise ConfigError(e)


