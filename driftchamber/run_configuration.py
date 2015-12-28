import yaml
from driftchamber.core.datastore import ObjectLifetime

class YamlConfiguration(object):
    
    def __init__(self, path, root_node):
        with open(path, 'r') as stream:
            data = yaml.load(stream)
            self._values = data.get(root_node)
        
    def get_value(self, key, default = None):
        return self._values.get(key) if key in self._values else default
    
class RunConfiguration(YamlConfiguration):
    
    def __init__(self, path):
        super().__init__(path, 'drift_chamber')

    def modules(self):
        modules = []
        def is_dict(obj): return isinstance(obj, dict)

        for mod in self.get_value('modules', []):
            param_name = mod.get('parameters') if is_dict(mod) else None
            
            modules.append({'cls': mod.get('class') if is_dict(mod) else mod, 
                            'params': self.parameters(param_name)})

        return modules

    def parameters(self, param_name):
        all_params = self.get_value('parameters', {})
        return all_params.get(param_name, {}) if param_name else {}
    
    def datastore_objects(self):
        return self.get_value('datastore_objects', {}).items()

class ResourceLoader(object):

    def load_module(self, cls_name, params = {}):
        cls_fqn = 'driftchamber.modules.{}'.format(cls_name)
        cls = self.load_class(cls_fqn)
        return cls(**params)

    def load_class(self, class_fqn):
        parts = class_fqn.split('.')
        module_name = '.'.join(parts[:-1])
        cls = __import__(module_name)
        
        for component in parts[1:]:
            cls = getattr(cls, component)

        return cls

    def load_object(self, config):
        params = {}
        is_dict = lambda obj: isinstance(obj, dict)

        for name, val in config.get('attr_values').items():
            params[name] = self.load_object(val) if is_dict(val) else val

        cls = self.load_class(config.get('class'))
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
            module = self._loader.load_module(m.get('cls'), m.get('params'))
            engine.add_module(module)

    def _add_datastore_objects(self, config, engine):
        for name, obj_config in config.datastore_objects():
            lifetime = ObjectLifetime[obj_config.get('lifetime')]
            obj = self._loader.load_object(obj_config)
            engine._datastore.put(name, obj, lifetime)
