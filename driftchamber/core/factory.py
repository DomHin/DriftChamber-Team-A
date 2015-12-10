__author__ = 'Genti Saliu'

from driftchamber.utils import String, Introspection

class ModuleFactory:
    
    MODULES_PACKAGE = 'driftchamber.modules'
    
    @staticmethod
    def create_instance(module_name):
        class_name = String.underscore_to_camelcase(module_name)
        class_fqn = '{0}.{1}.{2}'.format(ModuleFactory.MODULES_PACKAGE, module_name, class_name)
        cls = Introspection.get_class(class_fqn)
        
        return cls()
    
class DataFactory:
    
    DATA_PACKAGE = 'drifthamber.data'
    
    @staticmethod
    def create_instance(class_name, properties):
        pass