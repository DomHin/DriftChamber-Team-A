# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

from driftchamber.core.configuration.configuration_option import ConfigurationOption
from driftchamber.core.configuration.configuration_option_validation import ConfigurationOptionValidation


configuration_specification = {
'Tracking': [
    ConfigurationOption('precision',
                        'Decimal precision',
                        float,
                        [ConfigurationOptionValidation(
                            lambda value: value >= 0,
                            'The precision should be positive.'
                        )],
                        p_isCompulsory=True),
    ConfigurationOption('threshold',
                        'minimum hits in houghspace to generate Track',
                        int,
                        [ConfigurationOptionValidation(
                            lambda value: value >= 0,
                            'The threshold should be positive.'
                        )],
                        p_isCompulsory=True),
    ConfigurationOption('minDistance',
                        'minimum distance in houghspace from other Tracks',
                        int,
                        [ConfigurationOptionValidation(
                            lambda value: value >= 0,
                            'minDistance should be positive.'
                        )],
                        p_isCompulsory=True)
    ]
}