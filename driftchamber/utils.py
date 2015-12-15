class Introspection(object):
    
    def load_class(self, class_fqn):
        parts = class_fqn.split('.')
        module_name = '.'.join(parts[:-1])
        module = __import__(module_name)
        
        for component in parts[1:]:
            module = getattr(module, component)
        
        return module