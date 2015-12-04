from driftchamber.core.run_engine import RunEngine
import os
from importlib import import_module
from driftchamber.core.configuration.configuration import Configuration
from driftchamber.core.datastore import ObjectLifetime

class ModuleSpecification():
    def __init__(self, p_moduleName, p_pathToConfigurationFile = None):
        self.moduleName = p_moduleName
        self.pathToConfigurationFile = p_pathToConfigurationFile

class RunEngineFactory:
    def __init__(self, p_module_specifications, p_dataStore):
        self._module_specifications = p_module_specifications
        self._dataStore = p_dataStore
        self._init_modules()
        self._init_run_engine()
        
    def get_run_engine(self):
        return self._run_engine
        
    def _init_modules(self):
        self._modules = []
        for moduleSpecification in self._module_specifications:
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
                #if the module resides in a sub folder it can also have a specification for its configuration
                if os.path.exists(pathToConfigurationSpecification):
                    if moduleSpecification.pathToConfigurationFile is None:
                        raise ValueError("Module '" + moduleName + "' needs a configuration, but no file is specified.'")
                    moduleConfigurationSpecification = import_module(pathToConfigurationSpecification_py)
                    configurationSpecification = getattr(moduleConfigurationSpecification, 'configuration_specification')
                    moduleConfiguration = Configuration(moduleSpecification.pathToConfigurationFile, configurationSpecification)   
            module = import_module(pathToModule_py)
            className = moduleName[:-6]
            moduleInstance = getattr(module, className)()
            # store the configuration for each module in the data store using the instance of the module as key
            self._dataStore.put(moduleInstance, moduleConfiguration, ObjectLifetime.Application)
            self._modules.append(moduleInstance)
        
    def _init_run_engine(self):
        self._run_engine = RunEngine(self._modules, self._dataStore)
        