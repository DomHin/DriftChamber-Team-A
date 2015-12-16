import yaml

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
    
class RunConfiguration(YamlConfiguration):
    
    def __init__(self, path):
        super().__init__(path, 'drift_chamber')

class Loader(object):
    
    MODULES_PACKAGE = 'driftchamber.modules'
    DATA_PACKAGE = 'driftchamber.data'
    
    def load_module(self, module):
        cls_fqn = '%s.%s' % (self.MODULES_PACKAGE, module)
        cls = self.load_class(cls_fqn)
        
        return cls()
    
    def load_class(self, class_fqn):
        parts = class_fqn.split('.')
        module_name = '.'.join(parts[:-1])
        module = __import__(module_name)
        
        for component in parts[1:]:
            module = getattr(module, component)
        
        return module
    
    def load_datastore_object(self, config):
        pass
        
class RunEngineConfigurator(object):
    
    def __init__(self, loader):
        self._loader = loader
    
    def apply(self, config, engine):
        nr_events = config.get_value('nr_events')
        engine.nr_events = nr_events
        
        self._add_modules(config, engine)
        self._add_objects(config, engine)
            
    def _add_modules(self, config, engine):
        module_names = config.get_value('modules')
        
        for module_name in module_names:
            module = self._loader.load_module(module_name)
            engine.add_module(module)
    
    def _add_objects(self, config, engine):
        pass
        