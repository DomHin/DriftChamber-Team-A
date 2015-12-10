import yaml

class YamlConfiguration(object):

    def __init__(self, path, root_node):
        self.__parse_config(path, root_node)

    def __parse_config(self, path, root_node):
        stream = open(path, 'r')
        data = yaml.load(stream)

        self.__config = data[root_node]

class RunConfiguration(YamlConfiguration):

    ROOT_NODE = 'run_configuration'

    def __init__(self, path):
        super(path, self.ROOT_NODE)
        
    @property
    def nr_events(self):
        return self.__config.nr_events
    
    @property
    def object_paths(self):
        return self.__config.objects
    
    @property
    def module_names(self):
        return self.__config.modules
    
class ObjectConfiguration(YamlConfiguration):
    
    ROOT_NODE = 'object'
    
    def __init(self, path):
        super(path, self.ROOT_NODE)
        
    @property
    def id(self):
        return self.__config.id
    
    def type(self):
        return self.__config.type
    
    def lifetime(self):
        return self.__config.lifetime
    
    def attr_values(self):
        return self.__config.attr_values
    
class RunEngineConfigurator(object):
    
    MODULES_PACKAGE = 'driftchamber.modules'
    
    def __init__(self, string_utils, introspection_utils):
        self.__string_utils = string_utils
        self.__introspection_utils = introspection_utils
    
    def apply_run_configuration(self, run_configuration, run_engine):
        run_engine.nr_events(run_configuration.nr_events())
        
        self.__add_modules(run_configuration.module_names(), run_engine)
        self.__add_objects(run_configuration.object_paths(), run_engine)
            
    def __add_modules(self, module_names, run_engine):
        for module_name in module_names:
            module = self.__create_module_instance(module_name)
            run_engine.add_module(module)
    
    def __create_module_instance(self, module_name):
        module_cls = self.__string_utils.underscore_to_camelcase(module_name)
        module_cls_fqn = '{0}.{1}.{2}' % (self.MODULES_PACKAGE, module_name, module_cls)
        cls = self.__introspection_utils.get_class(module_cls_fqn)
        
        return cls()
    
    def __add_objects(self, object_paths, run_engine):
        obj_configurations = [self.__get_object_configuration(object_path) for object_path in object_paths]
        pass
    
    def __get_object_configuration(self, object_path):
        pass