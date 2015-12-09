from driftchamber.core.config.option import ConfigurationOption
from driftchamber.core.config.option_validation import ConfigurationOptionValidation


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
                        p_isCompulsory=True)
    ]
}