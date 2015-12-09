
from ast import literal_eval

from driftchamber.core.config.option import ConfigurationOption
from driftchamber.core.config.option_validation import ConfigurationOptionValidation


configuration_specification = {
'Detector': [
    ConfigurationOption('nSuperLayers',
                        'The number of super layers.',
                        int,
                        [ConfigurationOptionValidation(
                            lambda value: value > 0,
                            'The number of super layers has to be a positive integer.'
                        )],
                        p_isCompulsory=True),
    ConfigurationOption('nLayersList',
                        'List of layers per super layer.',
                        lambda value: literal_eval(value),
                        [ConfigurationOptionValidation(
                            lambda value: isinstance(value, list),
                            "'layers' has to be a list that can be parsed by python."),
                         ConfigurationOptionValidation(
                            lambda value: all(isinstance(nLayer, int) for nLayer in value),
                            "The amount of layers per super layer must be an integer."),
                         ConfigurationOptionValidation(
                            lambda value: all(nLayer > 0 for nLayer in value),
                            "The amount of layers per super layer must be a positive integer.")
                         ],
                        p_isCompulsory=True),
    ConfigurationOption('width',
                        'The width of the drift chamber.',
                        int,
                        [ConfigurationOptionValidation(
                            lambda value: value > 0,
                            'The width of the drift chamber has to be a positive integer.'
                        )],
                        p_isCompulsory=True)
    ]
}