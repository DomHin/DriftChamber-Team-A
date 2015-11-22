"""
Created on Nov 19, 2015

@author: Fabian Leven
"""

import os
from configparser import ConfigParser
from argparse import ArgumentParser
import re
import logging

def to_bool(p_value):
    """
    Helper function to convert a string to a boolean value.
    
    p_value must either be 'true' or 'false' in the right case.
    """
    if p_value == "true":
        return True
    elif p_value == "false":
        return False
    raise ValueError(
        ("Can not parse the configuration file "
         "because a boolean value is not specified as 'true' or 'false'."))


class _ConfigurationOption:
    """
    An option that can be configured.
    """
    
    
    def __init__(self, 
                 p_key,
                 p_description,
                 p_parseFunction = None, 
                 p_listOfTests = None,
                 p_isCompulsory = True):
        """
        Constructor.
        
        p_key              a unique identifier within the given section of the configuration.
        p_description      a description.
        p_parseFunction    a function to convert the configuration value ('string') 
                           to the desired format (e.g. 'int').
        p_listOfTests      a list of specifications the configuration value must satisfy, 
                           see examples below.
        p_isCompulsory     weather the configuration option must be present ('True') 
                           in the configuration or not ('False').
        """
        self.key = p_key
        self.description = p_description
        self.parseFunction = (lambda x: x) if p_parseFunction is None else p_parseFunction
        self.listOfTests = [] if p_listOfTests is None else p_listOfTests
        self.isCompulsory = p_isCompulsory
        # set later to enable a convenient way of entering options into the code
        self.section = ''
        
    def get_full_key(self):
        """
        ::return:: a unique identifier for this option.
        """
        return self.section + '_' + self.key
        
class _ConfigurationOptionValidation:
    """
    A validationFunction to check if the value specified for an option is valid.
    """
    def __init__(self,
                 p_validationFunction, 
                 p_failureMessage):
        """
        Constructor.
        p_validationFunction  a function that takes a value for an option as argument 
                              and evaluates to true if the value is valid, e.g.::
                                lambda value: value > 0
        p_failureMessage      an error message used in case the validation fails.
        """
        self.validationFunction = p_validationFunction
        self.failureMessage = p_failureMessage
                 

class Configuration:
    """
    The global configuration represented by key value pairs. 
    The values are loaded using the command line arguments.
    Example usage::
        configuration = Configuration()
        moduleNames = configuration["Modules_moduleSequence"]
    """
    
    def __init__(self, p_args = None):
        """
        Constructor.
        
        p_args      the command line arguments. 
                    Leave this to 'None' as it is only needed for testing purposes.
        """
        optionSpecifications = {
            "General": [ # section name to categorize the options in the configuration
            #_ConfigurationOption(
            #    "exampleKey",
            #    "description"
            #     # a function to interpret the configuration value, 
            #     # e.g. int, to_bool (see above), float, or a arbitrary lambda expression
            #     int, 
            #     [#A list of conditions the value must satisfy.
            #         _ConfigurationOptionValidation(lambda value: value > 0, 
            #                                        "This value must be greater than 0"),
            #         _ConfigurationOptionValidation(lambda value: value < 10, 
            #                                        "This value must be smaller than 10"),
            #     ]
            #     # weather the option must be present (True) in the configuration or not (False)
            #     False, 
            #),
                 _ConfigurationOption(
                    "nEvent",
                    "The amount of events to simulate. This has to be a positive integer.",
                    int, 
                    [
                     _ConfigurationOptionValidation(
                        lambda value: value > 0, 
                        "The amount of events must be a positive integer.")]),
                _ConfigurationOption(
                    "levelOfLogging",
                    ("The level of the logging. Must be one of the following: "
                     "'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'."),
                    lambda value: {'CRITICAL': logging.CRITICAL, 
                                    'ERROR': logging.ERROR, 
                                    'WARNING': logging.WARNING, 
                                    'INFO': logging.INFO, 
                                    'DEBUG': logging.DEBUG, 
                                    'NOTSET': logging.NOTSET}[value.upper()],
                    p_isCompulsory = False)
            ],
            "Modules":[                     
               _ConfigurationOption(
                    "moduleSequence",
                    ("A list of the module names that shall be executed by the run engine. "
                     "Separate the module names using commas or line breaks. "
                     "The corresponding module has to be present in the module folder. "
                     "In more detail, this means there must be a python file present called "
                     "'ModuleNameModule'. "
                     "It must hold a class called 'ModuleName' "
                     "(without the 'Module' at the end). "
                     "It must reside in the module folder."),
                     # The following expression splits the module name option at line breaks and 
                     # commas, strips the white spaces and removes empty entries.
                     # It uses that bool('') evaluates to 'False'.
                     # In short, a list of the module names is returned.
                     lambda value: 
                        list(
                            filter(
                                bool, 
                                [moduleName.strip() for moduleName in re.split(r'[,\n]+', value)]
                            )),
                    [
                        _ConfigurationOptionValidation(
                            lambda value: len(value) > 0, 
                            "There must be at least one module in the module sequence.")
                    ])
            ]     
        }
        
        # reorganize the specifications of the options from 
        # an "easy-to-type"-form to an "easy-to-handle-by-pc"-form
        self.optionSpecifications = []
        for configurationOptionSection, configurationOptions in optionSpecifications.items():
            for configurationOption in configurationOptions:
                configurationOption.section = configurationOptionSection
                self.optionSpecifications.append(configurationOption)
                
        # holds all the options as key value pairs
        self._options = dict()
        self._init_argument_parser()
        # the first parameter of parse_args will default to sys.argv if p_args is None
        # p_args is only used for testing purposes
        self._parsedArgs = vars(self._argumentParser.parse_args(p_args))
        
        self.hasConfigurationFile = self._try_init_configuration_file_parser()
        self._try_load_all_options()
        
        
    def _init_argument_parser(self):
        self._argumentParser = ArgumentParser('Drift Chamber Project of Team A')
        self._argumentParser.add_argument(
            '--config', 
            type=str,
            help='Path to a file that holds the configuration for this program run.')
        for configurationOption in self.optionSpecifications:
            self._argumentParser.add_argument(
                '--' + configurationOption.get_full_key(), 
                type=str, help=configurationOption.description, 
                required=False)
        
    
    def _try_init_configuration_file_parser(self):
        configKey = 'config'
        if not configKey in self._parsedArgs:
            return False
        self.configFileName = self._parsedArgs[configKey]
        if self.configFileName is None:
            return False
        if not os.path.isfile(self.configFileName):
            raise ValueError(
                "The specified configuration file " + 
                self.configFileName + " could not be found.")
        self.configFileParser = ConfigParser()
        self.configFileParser.read(self.configFileName)
        return True
    
    
    def _try_load_all_options(self):
        for configurationOption in self.optionSpecifications:
            if (
                not self._try_retrieve_option(configurationOption) and 
                configurationOption.isCompulsory):
                raise ValueError("The compulsory option '" + 
                                 configurationOption.key + 
                                 "' was not specified in the configuration.")
            
        
    def _try_retrieve_option(self, p_configurationOption):
        # first try to retrieve an option from the command line arguments, 
        # if that fails try the configuration file
        return (
            self._try_retrieve_option_from_command_line_arguments(p_configurationOption) or 
            (
                self.hasConfigurationFile and 
                self._try_retrieve_option_from_configuration_file(p_configurationOption)))
            
    
    def _try_retrieve_option_from_configuration_file(self, p_configurationOption):
        if (
            not self.hasConfigurationFile or 
            not self.configFileParser.has_option(p_configurationOption.section, 
                                                 p_configurationOption.key)):
            return False
        self._set_option_from_raw_value(p_configurationOption, 
                                        self.configFileParser.get(p_configurationOption.section, 
                                                                  p_configurationOption.key))
        return True
    
        
    def _try_retrieve_option_from_command_line_arguments(self, p_configurationOption):
        rawValue = self._parsedArgs[p_configurationOption.get_full_key()]
        if rawValue is None:
            return False
        self._set_option_from_raw_value(p_configurationOption, rawValue)
        return True
    
    
    def _set_option_from_raw_value(self, p_ConfigurationOption, p_rawValue):
        value = p_ConfigurationOption.parseFunction(p_rawValue)
        # calls all specified tests for a value, e.g. that it has to be an integer smaller than 5
        self._assure_option_integrity(p_ConfigurationOption, value)
        self._options[p_ConfigurationOption.get_full_key()] = value
        
    
    def _assure_option_integrity(self, p_configurationOption, p_value):
        for optionTest in p_configurationOption.listOfTests:
            if not optionTest.validationFunction(p_value):
                raise ValueError("Error while parsing configuration option '" + 
                                 p_configurationOption.key + "': " + 
                                 optionTest.failureMessage)
        
        
    def __getitem__(self, p_key):
        return self._options[p_key]