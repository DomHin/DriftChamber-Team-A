import yaml
from os import path

class YamlConfiguration(object):

    def __init__(self, path, root_node):
        self._path = path
        self._root_node = root_node
        self._values = {}
        
        self._parse()

    def _parse(self):
        stream = open(self._path, 'r')
        data = yaml.load(stream)
        self._values = data[self._root_node]
    
    def get_value(self, key):
        return self._values[key]

class Loader(object):
    
    MODULES_PACKAGE = 'driftchamber.modules'
    
    def __init(self, inflector, introspect):
        self._inflector = inflector
        self._introspect = introspect
    
    def load_module(self, module):
        cls_name = self._inflector.camelize(module)
        cls_fqn = '{0}.{1}' % (self.MODULES_PACKAGE, cls_name)
        cls = self._introspect.load_class(cls_fqn)
        
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
        