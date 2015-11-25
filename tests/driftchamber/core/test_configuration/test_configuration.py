# -*- coding: utf-8 -*-
"""
@author: Fabian Leven
"""

import logging
import os
import unittest

from driftchamber.core.configuration import Configuration


class ConfigurationTest(unittest.TestCase):
    """
    Test class for the Configuration class
    """
    
    def setUp(self):
        self.pathToConfgiFiles = (
            os.path.dirname(os.path.abspath(__file__)) + '/')

    def test_config_file_only(self):
        pathToConfigFile = self.pathToConfgiFiles + 'test_config_allOptions.cfg'
        configuration = Configuration(['--config', pathToConfigFile])
        self.assertEqual(configuration['General_nEvent'], 100)
        self.assertEqual(configuration['General_levelOfLogging'], logging.DEBUG)
        self.assertEqual(configuration['Modules_moduleSequence'], 
                         [['HelloWorldModule'], ['ByeByeWorldModule'], ['ParticleGunModule']])


    def test_config_file_not_found(self):
        self.assertRaises(ValueError, 
                          Configuration, ['--config', "thisIsARandomBliberBlubberPath"])
        
    
    def test_compulsory_option_missing(self):
        pathToConfigFile = self.pathToConfgiFiles + 'test_config_compulsoryOptionMissing.cfg'
        self.assertRaises(ValueError, Configuration, ['--config', pathToConfigFile])
        
        
    def test_optional_option_missing(self):
        pathToConfigFile = self.pathToConfgiFiles + 'test_config_optionalOptionMissing.cfg'
        Configuration(['--config', pathToConfigFile])
        
    
    def test_invalid_value(self):
        pathToConfigFile = self.pathToConfgiFiles + 'test_config_invalidValue.cfg'
        self.assertRaises(ValueError, Configuration, ['--config', pathToConfigFile])
        
        
    def test_only_command_line_arguments(self):
        configuration = Configuration(['--General_nEvent', 
                                       '100', 
                                       '--Modules_moduleSequence', 
                                       'HelloWorldModule\nByeByeWorldModule',
                                       '--General_levelOfLogging', 
                                       'DEBUG',
                                       '--Detector_superlayers', '1',
                                       '--Detector_layers', '[1]',
                                       '--Detector_width', '1'])
        self.assertEqual(configuration['General_nEvent'], 100)
        self.assertEqual(configuration['General_levelOfLogging'], logging.DEBUG)
        self.assertEqual(configuration['Modules_moduleSequence'], 
                         [['HelloWorldModule'], ['ByeByeWorldModule']])
        
        
    def test_command_line_arguments_override_config_file(self):
        pathToConfigFile = self.pathToConfgiFiles + 'test_config_allOptions.cfg'
        configuration = Configuration(['--config', 
                                       pathToConfigFile, 
                                       '--General_nEvent', 
                                       '101', 
                                       '--Modules_moduleSequence', 
                                       'HelloWorldModule'])
        self.assertEqual(configuration['General_nEvent'], 101)
        self.assertEqual(configuration['General_levelOfLogging'], logging.DEBUG)
        self.assertEqual(configuration['Modules_moduleSequence'], [['HelloWorldModule']])
        