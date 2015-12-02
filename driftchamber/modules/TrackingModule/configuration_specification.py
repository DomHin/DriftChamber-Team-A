# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

from driftchamber.core.configuration.configuration_option import ConfigurationOption
from driftchamber.core.configuration.configuration_option_validation import ConfigurationOptionValidation


configuration_specification = {
'Tracking': [
    ConfigurationOption('precission',
                        'Decimal precission',
                        int,
                        [ConfigurationOptionValidation(
                            lambda value: value >= 0,
                            'The precission should be positiv'
                        )],
                        p_isCompulsory=True)
    ]
}