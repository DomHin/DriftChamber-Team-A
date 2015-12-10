class String(object):
    
    def underscore_to_camelcase(self, value):
        def camelcase():
            while True:
                yield str.capitalize

        c = camelcase()
        return ''.join(next(c)(x) if x else '_' for x in value.split('_'))

class Introspection():
    
    def get_class(self, class_fqn):
        parts = class_fqn.split('.')
        module_name = '.'.join(parts[:-1])
        module = __import__(module_name)
        
        for component in parts[1:]:
            module = getattr(module, component)
        
        return module