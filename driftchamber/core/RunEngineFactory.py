from driftchamber.core.run_engine import RunEngine
import os
from importlib import import_module
from driftchamber.core.configuration.configuration import Configuration
from driftchamber.core.datastore import ObjectLifetime

class ModuleFactory():
    def __init__(self, 
                 p_moduleName, 
                 p_path_to_configuration_file = None, 
                 p_path_to_modules = 'modules/',
                 p_path_to_modules_py = 'driftchamber.modules.'):
        self._module_name = p_moduleName
        self._path_to_configuration_file = p_path_to_configuration_file
        self._path_to_modules = p_path_to_modules
        self._path_to_modules_py = p_path_to_modules_py
        self._init_module_paths()
        
        
    def _init_module_paths(self):
        self._path_to_configuration_spec = None
        self._path_to_configuration_spec_py = None
        self._path_to_module = self._path_to_modules + self._module_name
        self._path_to_module_py = self._path_to_modules_py + self._module_name
        # a module can either reside in a sub folder or in the module folder
        if os.path.isdir(self._path_to_module):
            self._path_to_configuration_spec = self._path_to_module + '/configuration_specification.py'
            if os.path.isfile(self._path_to_configuration_spec):
                self._path_to_configuration_spec_py = self._path_to_module_py + '.configuration_specification'
            else:
                self._path_to_configuration_spec = None
            self._path_to_module += '/' + self._module_name + '.py'
            self._path_to_module_py += '.' + self._module_name
        
        
    def get_module_configuration(self):
        if self._path_to_configuration_spec is None:
            if self._path_to_configuration_file is not None:
                raise ValueError("Module '" + self._module_name + "' must not have a configuration, but one is specified.'")
            return None
        if os.path.exists(self._path_to_configuration_spec):
            if self._path_to_configuration_file is None:
                raise ValueError("Module '" + self._module_name + "' needs a configuration, but no file is specified.'")
            configuration_spec_module = import_module(self._path_to_configuration_spec_py)
            configuration_spec = getattr(configuration_spec_module, 'configuration_specification')
            return Configuration(self._path_to_configuration_file, configuration_spec)
              

    def get_module_instance(self):
        module = import_module(self._path_to_module_py)
        className = self._module_name[:-6]
        return getattr(module, className)()
        

class RunEngineFactory:
    def __init__(self, p_module_factories, p_dataStore):
        self._module_factories = p_module_factories
        self._dataStore = p_dataStore
        self._init_modules()
        self._init_run_engine()
        
        
    def get_run_engine(self):
        return self._run_engine
    
        
    def _init_modules(self):
        self._modules = []
        for module_factory in self._module_factories:
            module_instance = module_factory.get_module_instance()
            self._dataStore.put(module_instance, module_factory.get_module_configuration(), ObjectLifetime.Application)
            self._modules.append(module_instance)
            
        
    def _init_run_engine(self):
        self._run_engine = RunEngine(self._modules, self._dataStore)
        