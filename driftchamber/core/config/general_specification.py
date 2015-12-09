"""
Created on Nov 19, 2015

@author: Fabian Leven
"""

import logging

from driftchamber.core.config.option import ConfigurationOption
from driftchamber.core.config.option_validation import ConfigurationOptionValidation
from driftchamber.core.config.parsing_functions import parse_module_sequence


driftChamberConfig_generalSpecification = {
"General": [ # section name to categorize the options in the configuration
#ConfigurationOption(
#    "exampleKey",
#    "description"
#     # a function to interpret the configuration value, 
#     # e.g. int, to_bool (see above), float, or a arbitrary lambda expression
#     int, 
#     [#A list of conditions the value must satisfy.
#         _ConfigurationOptionValidation(lambda value: value > 0, 
#                                        "This value must be greater than 0"),
#         _ConfigurationOptionValidation(lambda value: value < 10, 
#                                        "This value must be smaller than 10"),
#     ]
#     # weather the option must be present (True) in the configuration or not (False)
#     False, 
#),
    ConfigurationOption(
       "nEvent",
       "The amount of events to simulate. This has to be a positive integer.",
       int, 
       [
            ConfigurationOptionValidation(
                lambda value: value > 0, 
                "The amount of events must be a positive integer.")]),
    ConfigurationOption(
       "levelOfLogging",
       ("The level of the logging. Must be one of the following: "
        "'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'."),
       lambda value: {'CRITICAL': logging.CRITICAL, 
                       'ERROR': logging.ERROR, 
                       'WARNING': logging.WARNING, 
                       'INFO': logging.INFO, 
                       'DEBUG': logging.DEBUG, 
                       'NOTSET': logging.NOTSET}[value.upper()],
       p_isCompulsory = False)
],
"Modules":[                     
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
               "There must be at least one module in the module sequence.")
       ])
    ],
}