#! /usr/bin/env python3.4

import logging
from importlib import import_module
from driftchamber.core.configuration import Configuration
from driftchamber.core.run_engine import RunEngine
import traceback


class DriftChamber:
    '''
    Objects of this class represent an instance of the program. It manages the general program flow.
    
    args     The command line arguments. Only use this for testing purposes and let it default to sys.argv otherwise.
    '''
    def __init__(self, args = None):
        # The configuration class also parses the command line arguments.
        # Hence, in order for the argument parser to be the first to stream to the standard output. No output should be streamed before the next line is executed.
        self._configuration = Configuration(args)
        logging.basicConfig(level=self._configuration["General_levelOfLogging"])
        self._modules = []
        self._runEngine = None
        self._instantiateModules()
        
    def getConfiguration(self):
        return self._configuration

        
    def _instantiateModules(self):
        for moduleName in self._configuration["Modules_moduleSequence"]:
            module = import_module('driftchamber.modules.' + moduleName)
            className = moduleName[:-6]
            # this creates an instance of the module class
            self._modules.append(getattr(module, className)())
            
        
    def startSimulation(self):
        logging.info("'Drift Chamber Simulation' started.")
        self._runEngine = RunEngine(self, self._configuration["General_nEvent"])
        for module in self._modules:
            self._runEngine.add_module(module)
        self._runEngine.run()
        logging.info("'Drift Chamber Simulation' done.")
        

def main(args = None):
    '''
    Program entry point.
    
    args     The command line arguments. Only use this for testing purposes and let it default to sys.argv otherwise.
    '''
    # This is the default logging level. It can be adapted using the configuration key 'levelOfLogging'.
    logging.basicConfig(level=logging.NOTSET)
    try:
        driftChamber = DriftChamber(args)
        driftChamber.startSimulation()
    except Exception:
        logging.error('Fatal error: \n' + traceback.format_exc())
        # no reraise because the program will terminate anyway and we want our logging mechanism to handle all exceptions
    

if __name__ == '__main__':
    main()
