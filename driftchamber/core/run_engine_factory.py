#! /usr/bin/env python3.4
import os
from importlib import import_module

from driftchamber.core.run_engine import RunEngine
from driftchamber.core.configuration.configuration import Configuration
from driftchamber.core.datastore import ObjectLifetime


class ModuleFactory:
    """
    Instantiates modules and the corresponding configurations.
    """
    def __init__(self, 
                 p_module_name, 
                 p_path_to_configuration_file = None, 
                 p_path_to_modules = 'modules/',
                 p_path_to_modules_py = 'driftchamber.modules.'):
        """
        :param: p_module_name                   the name of the module as string,
                                                e.g. 'HelloWorldModule'
        :param: p_path_to_configuration_file    the configuration file for the module,
                                                e.g. '../configuration/my_module.cfg'
        :param: p_path_to_modules               the path to the folder holding the modules.  
                                                This can be changed for testing reasons, as 
                                                test modules might not reside in
                                                the standard module folder. Must end in '/'.
        :param: p_path_to_modules_py            the package path relative to the modules.
                                                This corresponds to p_path_to_modules but might
                                                be relative to an other origin. Must end in '.'.
        """
        self._module_name = p_module_name
        self._path_to_configuration_file = p_path_to_configuration_file
        self._path_to_modules = p_path_to_modules
        self._path_to_modules_py = p_path_to_modules_py
        self._init_module_paths()
        self._module = None
        self._CONFIGURATION_NOT_INSTANTIATED = -1
        self._configuration = self._CONFIGURATION_NOT_INSTANTIATED
        
        
    def _init_module_paths(self):
        self._path_to_configuration_spec = None
        self._path_to_configuration_spec_py = None
        self._path_to_module = self._path_to_modules + self._module_name
        self._path_to_module_py = self._path_to_modules_py + self._module_name
        # a module can either reside in a sub folder or in the module folder
        if os.path.isdir(self._path_to_module):
            # if it resides in a sub folder, it might need a configuration
            self._path_to_configuration_spec = (
                self._path_to_module + '/configuration_specification.py')
            if os.path.isfile(self._path_to_configuration_spec):
                self._path_to_configuration_spec_py = (
                    self._path_to_module_py + '.configuration_specification')
            else:
                self._path_to_configuration_spec = None
            self._path_to_module += '/' + self._module_name + '.py'
            self._path_to_module_py += '.' + self._module_name
        
        
    def get_module_configuration(self):
        """
        Instantiates and returns the configuration for the module.
        Will always return the same instance.
        :return: the configuration for the module
        """
        if self._configuration is self._CONFIGURATION_NOT_INSTANTIATED:
            #check if module needs configuration
            if self._path_to_configuration_spec is None:
                #no configuration needed
                if self._path_to_configuration_file is not None:
                    raise ValueError("Module '" + 
                                     self._module_name + 
                                     "' must not have a configuration, but one is specified.'")
                self._configuration = None
            else:
                #configuration needed
                if self._path_to_configuration_file is None:
                    raise ValueError("Module '" + 
                                     self._module_name + 
                                     "' needs a configuration, but no file is specified.'")
                configuration_spec_module = import_module(self._path_to_configuration_spec_py)
                configuration_spec = getattr(configuration_spec_module, 
                                             'configuration_specification')
                self._configuration = Configuration(self._path_to_configuration_file,
                                                    configuration_spec)
        return self._configuration
              

    def get_module_instance(self):
        """
        Instantiates and returns the module.
        Will always return the same instance.
        :return: the module
        """
        if self._module is None:
            module_py = import_module(self._path_to_module_py)
            class_name = self._module_name[:-6]
            self._module = getattr(module_py, class_name)()
        return self._module
        

class RunEngineFactory:
    """
    Creates a run engine and all its modules.
    """
    def __init__(self, p_module_factories, p_data_store):
        """
        Ctor.
        
        :param: p_module_factories      a list of the factories for the modules, 
                                        see class ModuleFactory.
        :param: p_data_store             the data store for the run engine
        """
        self._module_factories = p_module_factories
        self._dataStore = p_data_store
        self._init_modules()
        self._init_run_engine()
        
        
    def get_run_engine(self):
        """
        :returns: the set up run engine.
        """
        return self._run_engine
    
        
    def _init_modules(self):
        self._modules = []
        for module_factory in self._module_factories:
            module_instance = module_factory.get_module_instance()
            self._dataStore.put(module_instance, module_factory.get_module_configuration(), ObjectLifetime.Application)
            self._modules.append(module_instance)
            
        
    def _init_run_engine(self):
        self._run_engine = RunEngine(self._modules, self._dataStore)
        