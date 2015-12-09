"""
Created on Nov 26, 2015

@author: Fabian Leven
"""
from driftchamber.core.run_engine_factory import ModuleFactory

def to_bool(p_value):
    """
    Helper function to convert a string to a boolean value.
    
    p_value must either be 'true' or 'false' in the right case.
    """
    if p_value == "true":
        return True
    elif p_value == "false":
        return False
    raise ValueError(
        ("Can not parse the configuration file "
         "because a boolean value is not specified as 'true' or 'false'."))
    
def parse_module_sequence(p_value):
    """
    Parses the module sequence in the configuration file.
    
    :return: a list of ModuleFactory objects.
    """
    result = []
    lines = p_value.split('\n')
    for line in lines:
        line.strip()
        if len(line) == 0:
            continue
        moduleConfiguration_str = line.split(' ')
        #remove empty entries
        moduleConfiguration_str = list(filter(bool, moduleConfiguration_str))
        moduleName = moduleConfiguration_str[0]
        modulePathConfigurationFile = None
        if len(moduleConfiguration_str) > 1:
            modulePathConfigurationFile = moduleConfiguration_str[1]
        result.append(ModuleFactory(moduleName, modulePathConfigurationFile))
    return result
        
        