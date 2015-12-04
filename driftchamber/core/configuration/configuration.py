"""
Created on Nov 19, 2015

@author: Fabian Leven
"""

import os
from configparser import ConfigParser
                 

class Configuration:
    """
    A configuration represented by key value pairs. 
    Example usage::
        configuration = Configuration("config.cfg", ['General':ConfigurationOption('nEvent','The number of events.',int)])
        moduleNames = configuration["General_nEvent"]
    """
    
    def __init__(self, p_path_to_configuration_file, p_specification):
        """
        Constructor.
        
        :param p_path_to_configuration_file       the path to the configuration file.
        :param p_specification                 meta data about the configuration,
                                                e.g. which options have to be specified 
                                                and which values they can take
        """
        self._pathToConfiguratioFile = p_path_to_configuration_file
        
        # reorganize the specification of the options from 
        # an "easy-to-type"-form to an "easy-to-handle-by-pc"-form
        self.specification = []
        for configurationOptionSection, configurationOptions in p_specification.items():
            for configurationOption in configurationOptions:
                configurationOption.section = configurationOptionSection
                self.specification.append(configurationOption)
                
        # holds all the options as key value pairs
        self._options = dict()
        self.hasConfigurationFile = self._try_init_configuration_file_parser()
        self._try_load_all_options()
                
    
    def _try_init_configuration_file_parser(self):
        if not os.path.isfile(self._pathToConfiguratioFile):
            raise ValueError(
                "The specified configuration file " + 
                self._pathToConfiguratioFile + " could not be found.")
        self.configFileParser = ConfigParser()
        self.configFileParser.read(self._pathToConfiguratioFile)
        return True
    
    
    def _try_load_all_options(self):
        for configurationOption in self.specification:
            if (
                not self._try_retrieve_option(configurationOption) and 
                configurationOption.isCompulsory):
                raise ValueError("The compulsory option '" + 
                                 configurationOption.key + 
                                 "' was not specified in the configuration.")
            
        
    def _try_retrieve_option(self, p_configurationOption):
        return (self.hasConfigurationFile and 
                self._try_retrieve_option_from_configuration_file(p_configurationOption))
            
    
    def _try_retrieve_option_from_configuration_file(self, p_configurationOption):
        if (not self.hasConfigurationFile or 
            not self.configFileParser.has_option(p_configurationOption.section, 
                                                 p_configurationOption.key)):
            return False
        self._set_option_from_raw_value(p_configurationOption, 
                                        self.configFileParser.get(p_configurationOption.section, 
                                                                  p_configurationOption.key))
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