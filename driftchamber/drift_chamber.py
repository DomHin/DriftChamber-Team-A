#! /usr/bin/env python3.4

import logging
import traceback
from importlib import import_module

from driftchamber.core.configuration import Configuration
from driftchamber.core.run_engine import RunEngine


class DriftChamber:
    """
    Objects of this class represent an instance of the program.
    """
    def __init__(self, args = None):
        """
        Constructor.
        
        args     The command line arguments. Only use this for testing purposes and let it default to sys.argv otherwise.
        """
        # The configuration class also parses the command line arguments.
        # Hence, in order for the argument parser to be the first to stream to the standard output. No output should be streamed before the next line is executed.
        self._configuration = Configuration(args)
        logging.basicConfig(level=self._configuration["General_levelOfLogging"])
        self._modules = []
        self._runEngine = None
        self._instantiate_modules()
        
        
    def get_configuration(self):
        return self._configuration

        
    def _instantiate_modules(self):
        for moduleName in self._configuration["Modules_moduleSequence"]:
            module = import_module('driftchamber.modules.' + moduleName)
            className = moduleName[:-6]
            # this creates an instance of the module class
            self._modules.append(getattr(module, className)())
            
        
    def start_simulation(self):
        logging.info("'Drift Chamber Simulation' started.")
        self._runEngine = RunEngine(self._configuration["General_nEvent"], self._modules, self)
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
