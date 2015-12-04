"""
Created on Nov 19, 2015

@author: Fabian Leven
"""

from driftchamber.core.configuration.configuration_option import ConfigurationOption
from driftchamber.core.configuration.configuration_option_validation import ConfigurationOptionValidation
from driftchamber.core.configuration.parsing_functions import parse_module_sequence


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
       ]),
    ],
}