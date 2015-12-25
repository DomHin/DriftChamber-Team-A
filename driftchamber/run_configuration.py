import yaml
from driftchamber.core.datastore import ObjectLifetime

class YamlConfiguration(object):
    
    def __init__(self, path, root_node):
        stream = open(path, 'r')
        data = yaml.load(stream)
        self._values = data[root_node]
        
    def get_value(self, key, default = None):
        return self._values[key] if key in self._values else default
    
class RunConfiguration(YamlConfiguration):
    
    def __init__(self, path):
        super().__init__(path, 'drift_chamber')

    def modules(self):
        modules = []
        is_dict = lambda obj: isinstance(obj, dict)
        parameters = lambda name: self.get_value('parameters')[name]
        
        for m in self.get_value('modules', []):
            module = {
                'cls': m['class'] if is_dict(m) else m,
                'params': parameters(m['parameters']) \
                            if is_dict(m) and 'parameters' in m else {}
            }
            modules.append(module)
        
        return modules

class Loader(object):
    
    MODULES_PACKAGE = 'driftchamber.modules'
    
    def load_module(self, cls_name, params = {}):
        cls_fqn = '{}.{}'.format(self.MODULES_PACKAGE, cls_name)
        cls = self.load_class(cls_fqn)
        return cls(**params)

    def load_class(self, class_fqn):
        parts = class_fqn.split('.')
        module_name = '.'.join(parts[:-1])
        cls = __import__(module_name)
        
        for component in parts[1:]:
            cls = getattr(cls, component)

        return cls

    def deserialize_object(self, config):
        params = {}
        is_dict = lambda obj: isinstance(obj, dict)

        for name, val in config['attr_values'].items():
            params[name] = self.deserialize_object(val) \
                                if is_dict(val) else val

        cls = self.load_class(config['class'])
        return cls(**params)
        
class RunEngineConfigurator(object):
    
    def __init__(self, loader):
        self._loader = loader

    def apply(self, config, engine):
        engine.events = config.get_value('events', 0)
        self._add_modules(config, engine)
        self._add_datastore_objects(config, engine)
            
    def _add_modules(self, config, engine):
        for m in config.modules():
            module = self._loader.load_module(m['cls'], m['params'])
            engine.add_module(module)

    def _add_datastore_objects(self, config, engine):
        datastore_objects = config.get_value('datastore_objects', {}).items()

        for name, obj_config in datastore_objects:
            lifetime = ObjectLifetime[obj_config['lifetime']]
            obj = self._loader.deserialize_object(obj_config)
            engine._datastore.put(name, obj, lifetime)
