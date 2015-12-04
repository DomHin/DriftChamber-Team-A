"""
Created on Nov 19, 2015

@author: Fabian Leven
"""

from driftchamber.core.configuration.configuration_option import ConfigurationOption
from driftchamber.core.configuration.configuration_option_validation import ConfigurationOptionValidation
from driftchamber.core.run_engine_factory import ModuleFactory

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
        result.append(ModuleFactory(moduleName, 
                                    modulePathConfigurationFile,
                                    "tests/driftchamber/modules/test_multiModule/",
                                    "tests.driftchamber.modules.test_multiModule."
                                    ))
    return result


configuration_specification = {
"MultiModule":[                     
    ConfigurationOption(
       "moduleSequence",
       ("A list of the module names that shall be executed by the run engine. "
        "Separate the module names using line breaks. "
        "The corresponding module has to be present in the module folder. "
        "In more detail, this means there must be a python file present called "
        "'ModuleNameModule' in the module folder in a sub folder also called "
        "'ModuleNameModule'. "
        "It must hold a class called 'ModuleName' "
        "(without the 'Module' at the end)."),
       parse_module_sequence,
       [
           ConfigurationOptionValidation(
               lambda value: len(value) > 0, 
               "There must be at least one module in the module sequence of the 'MultiModule'.")
       ])
    ],
}