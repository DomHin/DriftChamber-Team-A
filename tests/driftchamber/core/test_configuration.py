# -*- coding: utf-8 -*-
"""
@author: Fabian Leven
"""

import unittest
from driftchamber.core.configuration import Configuration
import os
import logging


class ConfigurationTest(unittest.TestCase):
    """
    Test class for the Configuration class
    """
    
    def setUp(self):
        self.pathToConfgiFiles = os.path.dirname(os.path.abspath(__file__))

    def test_onlyConfigFile(self):
        pathToConfigFile = self.pathToConfgiFiles+'/../../../configurations/test_config_allOptions.cfg'
        configuration = Configuration(['--config', pathToConfigFile])
        self.assertEqual(configuration['General_nEvent'], 100)
        self.assertEqual(configuration['General_levelOfLogging'], logging.DEBUG)
        self.assertEqual(configuration['Modules_moduleSequence'], ['HelloWorldModule', 'ByeByeWorldModule'])


    def test_configFileNotFound(self):
        self.assertRaises(ValueError, Configuration, ['--config', "thisIsARandomBliberBlubberPath"])
        
    
    def test_compulsoryOptionMissing(self):
        pathToConfigFile = self.pathToConfgiFiles+'/../../../configurations/test_config_compulsoryOptionMissing.cfg'
        self.assertRaises(ValueError, Configuration, ['--config', pathToConfigFile])
        
        
    def test_optionalOptionMissing(self):
        pathToConfigFile = self.pathToConfgiFiles+'/../../../configurations/test_config_optionalOptionMissing.cfg'
        Configuration(['--config', pathToConfigFile])
        
    
    def test_invalidValue(self):
        pathToConfigFile = self.pathToConfgiFiles+'/../../../configurations/test_config_invalidValue.cfg'
        self.assertRaises(ValueError, Configuration, ['--config', pathToConfigFile])
        
        
    def test_onlyCommandLineArguments(self):
        configuration = Configuration(['--General_nEvent', '100', '--Modules_moduleSequence', 'HelloWorldModule,ByeByeWorldModule', '--General_levelOfLogging', 'DEBUG'])
        self.assertEqual(configuration['General_nEvent'], 100)
        self.assertEqual(configuration['General_levelOfLogging'], logging.DEBUG)
        self.assertEqual(configuration['Modules_moduleSequence'], ['HelloWorldModule', 'ByeByeWorldModule'])
        
        
    def test_commandLineArgumentsOverrideConfigFile(self):
        pathToConfigFile = self.pathToConfgiFiles+'/../../../configurations/test_config_allOptions.cfg'
        configuration = Configuration(['--config', pathToConfigFile, '--General_nEvent', '101', '--Modules_moduleSequence', 'HelloWorldModule'])
        self.assertEqual(configuration['General_nEvent'], 101)
        self.assertEqual(configuration['General_levelOfLogging'], logging.DEBUG)
        self.assertEqual(configuration['Modules_moduleSequence'], ['HelloWorldModule'])
        