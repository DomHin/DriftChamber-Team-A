import yaml
from os import path

class YamlConfiguration(object):

    def __init__(self, path, root_node):
        self._path = path
        self._values = {}
        
        self._parse(root_node)

    def _parse(self, path, root_node):
        stream = open(self._path, 'r')
        data = yaml.load(stream)

        self._values = data[root_node]

    @property
    def path(self):
        return self._path
    
    def get_value(self, key):
        return self._values[key]

class RunConfiguration(object):

    def __init__(self, path):
        self._config = YamlConfiguration(root_node = 'run_configuration')
        
    @property
    def nr_events(self):
        return self._config.get_value('nr_events')
    
    @property
    def datastore_objects(self):
        return self._config.get_value('datastore_objects')
    
    @property
    def module_names(self):
        return self._config.get_value('modules')
    
class DataStoreObjectConfiguration(object):
    
    def __init(self, path):
        self._config = YamlConfiguration(root_node = 'datastore_objects')
        
    @property
    def id(self):
        return self._config.get_value('id')
    
    @property
    def class_name(self):
        return self._config.get_value('class')
    
    @property
    def lifetime(self):
        return self._config.get_value('lifetime')
    
    @property
    def attr_values(self):
        return self._config.get_value('attr_values')

class Loader(object):
    
    MODULES_PACKAGE = 'driftchamber.modules'
    
    def __init(self, inflector, introspect):
        self._inflector = inflector
        self._introspect = introspect
    
    def load_module(self, module):
        module_cls = self._inflector.camelize(module)
        module_cls_fqn = '{0}.{1}' % (self.MODULES_PACKAGE, module_cls)
        cls = self._introspect.load_class(module_cls_fqn)
        
        return cls()
    
    def load_datastore_object(self, config):
        pass
        
class RunEngineConfigurator(object):
    
    def __init__(self, loader):
        self._loader = loader
    
    def apply(self, run_config, run_engine):
        nr_events = run_config.nr_events()
        run_engine.nr_events(nr_events)
        
        self._add_modules(run_config, run_engine)
        self._add_objects(run_config, run_engine)
            
    def _add_modules(self, run_config, run_engine):
        for module_name in run_config.module_names():
            module = self._loader.load_module(module_name)
            run_engine.add_module(module)
    
    def _add_objects(self, run_config, run_engine):
        run_config_dir = path.dirname(path.realpath(run_config.path()))
        