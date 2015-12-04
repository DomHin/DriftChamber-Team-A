#! /usr/bin/env python3.4

import logging
import traceback
from argparse import ArgumentParser


from driftchamber.core.configuration.configuration import Configuration
from driftchamber.core.configuration.config_general_specification import driftChamberConfig_generalSpecification
from driftchamber.core.datastore import DataStore
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.run_engine_factory import RunEngineFactory


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
        
            
    def _init_run_engine(self):
        self._run_engine = RunEngineFactory(self._configuration["Modules_moduleSequence"], self._dataStore).get_run_engine()
            
        
    def start_simulation(self):
        logging.info("'Drift Chamber Simulation' started.")
        self._run_engine.log_configuration()
        self._run_engine.run()
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
