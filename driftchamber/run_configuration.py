import yaml
from os import path

class YamlConfiguration(object):

    def __init__(self, path, root_node):
        self._values = {}
        self._path = path
        self._root_node = root_node
        
        self._parse()

    def _parse(self):
        stream = open(self._path, 'r')
        data = yaml.load(stream)
        self._values = data[self._root_node]
    
    def get_value(self, key):
        return self._values[key]

class Loader(object):
    
    MODULES_PACKAGE = 'driftchamber.modules'
    DATA_PACKAGE = 'driftchamber.data'
    
    def __init__(self, introspect):
        self._introspect = introspect
    
    def load_module(self, module):
        cls_fqn = '%s.%s' % (self.MODULES_PACKAGE, module)
        cls = self._introspect.load_class(cls_fqn)
        
        return cls()
    
    def load_datastore_object(self, config):
        pass
        
class RunEngineConfigurator(object):
    
    def __init__(self, loader):
        self._loader = loader
    
    def apply(self, config, engine):
        nr_events = config.nr_events()
        engine.nr_events(nr_events)
        
        self._add_modules(config, engine)
        self._add_objects(config, engine)
            
    def _add_modules(self, config, engine):
        for module_name in config.module_names():
            module = self._loader.load_module(module_name)
            engine.add_module(module)
    
    def _add_objects(self, config, engine):
        run_config_dir = path.dirname(path.realpath(config.path()))
        