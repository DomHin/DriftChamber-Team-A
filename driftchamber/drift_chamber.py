#! /usr/bin/env python3.4

import logging
import traceback
from importlib import import_module
from argparse import ArgumentParser
import os

from driftchamber.core.configuration.configuration import Configuration
from driftchamber.core.configuration.config_general_specification import driftChamberConfig_generalSpecification
from driftchamber.core.run_engine import RunEngine
from driftchamber.core.datastore import DataStore
from driftchamber.core.datastore import ObjectLifetime


class DriftChamber:
    """
    Objects of this class represent an instance of the program.
    """
    def __init__(self, p_args = None):
        """
        Constructor.
        
        :param p_args     The command line arguments. Only use this for testing purposes and let it default to sys.argv otherwise.
        """
        
        # The configuration class also parses the command line arguments.
        # Hence, in order for the argument parser to be the first to stream to the standard output. No output should be streamed before the next line is executed.
        self._args = p_args
        self._init_commandline_argument_parser()
        self._init_confiuration()
        self._init_data_store()
        self._init_modules()
        self._init_run_engine()      
        
        
    def _init_commandline_argument_parser(self):
        self._commandLineKeyOfConfigurationFile = "config"
        self._commandLineFlagOfConfigurationFile = "--" + self._commandLineKeyOfConfigurationFile
        self._argumentParser = ArgumentParser('Drift Chamber Project of Team A')
        self._argumentParser.add_argument(
            self._commandLineFlagOfConfigurationFile, 
            type=str,
            help='Path to a file that holds the configuration for this program run.')
        self._parsedArgs = vars(self._argumentParser.parse_args(self._args))
        
        
    def _init_confiuration(self):
        self._configuration = Configuration(
            self._parsedArgs[self._commandLineKeyOfConfigurationFile],
            driftChamberConfig_generalSpecification)
        
        
    def _init_data_store(self):
        self._dataStore = DataStore()
        self._dataStore.put('nEvent', self._configuration['General_nEvent'], ObjectLifetime.Application)
        self._dataStore.put('configuration', self._configuration, ObjectLifetime.Application)
        self._dataStore.put('driftChamber', self, ObjectLifetime.Application)
        
        
    def _init_modules(self):
        self._modules = []
        for moduleSpecification in self._configuration["Modules_moduleSequence"]:
            moduleName = moduleSpecification.moduleName
            moduleConfiguration = None 
            pathToModule_py = 'driftchamber.modules.' + moduleName
            pathToModule = 'modules/' + moduleName
            # a module can either reside in a sub folder or in the module folder
            if os.path.isdir(pathToModule):
                pathToConfigurationSpecification_py = pathToModule_py + '.configuration_specification'
                pathToConfigurationSpecification = pathToModule + '/configuration_specification.py'
                pathToModule_py += '.' + moduleName
                pathToModule += '/' + moduleName
                if os.path.exists(pathToConfigurationSpecification):
                    if moduleSpecification.pathToConfigurationFile is None:
                        raise ValueError("Module '" + moduleName + "' needs a configuration, but no file is specified.'")
                    moduleConfigurationSpecification = import_module(pathToConfigurationSpecification_py)
                    configurationSpecification = getattr(moduleConfigurationSpecification, 'configuration_specification')
                    moduleConfiguration = Configuration(moduleSpecification.pathToConfigurationFile, configurationSpecification)   
            module = import_module(pathToModule_py)
            className = moduleName[:-6]
            moduleInstance = getattr(module, className)()
            self._dataStore.put(moduleInstance, moduleConfiguration, ObjectLifetime.Application)
            self._modules.append(moduleInstance)
    
            
    def _init_run_engine(self):
        self._runEngine = RunEngine(self._modules, self._dataStore)
            
        
    def start_simulation(self):
        logging.info("'Drift Chamber Simulation' started.")
        self._runEngine.run()
        logging.info("'Drift Chamber Simulation' done.")
        

def main(args = None):
    """
    Program entry point.
    
    args     The command line arguments. Only use this for testing purposes and let it default to sys.argv otherwise.
    """
    # This is the default logging level. It can be adapted using the configuration key 'levelOfLogging'.
    logging.basicConfig(level=logging.NOTSET)
    try:
        driftChamber = DriftChamber(args)
        driftChamber.start_simulation()
    except Exception:
        logging.error('Fatal error: \n' + traceback.format_exc())
        # no reraise because the program will terminate anyway and we want our logging mechanism to handle all exceptions
    

if __name__ == '__main__':
    main()
