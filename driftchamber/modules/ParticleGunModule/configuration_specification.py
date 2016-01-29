from driftchamber.core.configuration.configuration_option import ConfigurationOption
from driftchamber.core.configuration.configuration_option_validation import ConfigurationOptionValidation


configuration_specification = {
'Particle': [
    ConfigurationOption('mass',
                        'The mass of the particle in GeV.',
                        float,
                        [ConfigurationOptionValidation(
                            lambda value: value > 0,
                            'The mass of the particle must be positive.'
                        )],
                        p_isCompulsory=True),
    ConfigurationOption('name',
                        'The name of a particle.',
                        lambda value: str(value),
                        p_isCompulsory=True),
    ConfigurationOption('max_mom',
                        'The maximum momentum of a particle in GeV.',
                        float,
                        [ConfigurationOptionValidation(
                            lambda value: value > 0,
                            'The maximum momentum of a particle must be positive.'
                        )],
                        p_isCompulsory=True),
    ConfigurationOption('x_pos',
                        'The initial x-position of the particle in cells of the detector',
                        int,
                        p_isCompulsory=True),
        ConfigurationOption('y_pos',
                        'The initial y-position of the particle in cells of the detector',
                        int,
                        p_isCompulsory=True),
    ConfigurationOption('x_mom',
                        'The momentum of the particle in GeV',
                        float,
                        p_isCompulsory=True),
    ConfigurationOption('y_mom',
                        'The momentum of the particle in GeV',
                        float,
                        p_isCompulsory=True),
    ]
}