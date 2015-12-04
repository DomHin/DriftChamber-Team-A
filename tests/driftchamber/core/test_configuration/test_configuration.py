# -*- coding: utf-8 -*-
"""
@author: Fabian Leven
"""

import os
import unittest

from driftchamber.core.configuration.configuration import Configuration
from driftchamber.core.configuration.configuration_option import ConfigurationOption
from driftchamber.core.configuration.configuration_option_validation import ConfigurationOptionValidation
from driftchamber.core.configuration.parsing_functions import to_bool, parse_module_sequence, ModuleFactory



class ConfigurationTest(unittest.TestCase):
    """
    Test class for the Configuration class
    """
    
    def setUp(self):
        self.pathToConfgiFiles = os.path.dirname(os.path.abspath(__file__))
        self.pathToDefaultTestConfigFile = self.pathToConfgiFiles + '/test_config.cfg'
        self.defaultSpec = {
            "Section1": [ 
                ConfigurationOption(
                    "aPositiveInt",
                    "",
                    int, 
                    [
                        ConfigurationOptionValidation(
                            lambda value: value > 0, 
                            "This value must be positive.")]),
                ConfigurationOption(
                    "aNegativeInt",
                    "",
                    int, 
                    [
                        ConfigurationOptionValidation(
                            lambda value: value < 0, 
                            "This value must be negative.")]),
                ConfigurationOption(
                    "aBoolean",
                    "",
                    to_bool)
            ],
            "Section2": [ 
                ConfigurationOption(
                    "aPositiveInt",
                    "",
                    int, 
                    [
                        ConfigurationOptionValidation(
                            lambda value: value > 0, 
                            "This value must be positive.")]),
                ConfigurationOption(
                    "aNegativeInt",
                    "",
                    int, 
                    [
                        ConfigurationOptionValidation(
                            lambda value: value < 0, 
                            "This value must be negative.")]),
                ConfigurationOption(
                    "aFloat",
                    "",
                    float),
                ConfigurationOption(
                    "aBoolean",
                    "",
                    to_bool)
            ],  
        }

    def test_config_file_standard_types(self):
        configuration = Configuration(self.pathToDefaultTestConfigFile, self.defaultSpec)
        self.assertEqual(configuration['Section1_aPositiveInt'], 100)
        self.assertEqual(configuration['Section1_aNegativeInt'], -100)
        self.assertEqual(configuration['Section1_aBoolean'], True)
        self.assertEqual(configuration['Section2_aPositiveInt'], 100)
        self.assertEqual(configuration['Section2_aNegativeInt'], -100)
        self.assertEqual(configuration['Section2_aFloat'], 0.5)
        self.assertEqual(configuration['Section2_aBoolean'], False)


    def test_config_file_not_found(self):
        self.assertRaises(ValueError, Configuration, "randomPathBlibberBlubber", self.defaultSpec)
        
    
    def test_compulsory_option_missing(self):
        spec = {
            'Section1': [
                ConfigurationOption(
                    "thisIsCompulsory",
                    "",
                    to_bool,
                    p_isCompulsory=True)
            ]
        }
        self.assertRaises(ValueError, Configuration, self.pathToDefaultTestConfigFile, spec)
        
        
    def test_optional_option_missing(self):
        spec = {
            'Section1': [
                ConfigurationOption(
                    "thisIsOptional",
                    "",
                    to_bool,
                    p_isCompulsory=False)
            ]
        }
        Configuration(self.pathToDefaultTestConfigFile, spec)
        
    
    def test_invalid_value(self):
        spec = {
            "Section1": [ 
                ConfigurationOption(
                    "aPositiveInt",
                    "",
                    int, 
                    [
                        ConfigurationOptionValidation(
                            lambda value: value > 200, 
                            "This value must be very large.")])
            ]
        }
        self.assertRaises(ValueError, Configuration, self.pathToDefaultTestConfigFile, spec)
        
    
    def test_parsing_of_module_sequence(self):
        testConfig = (
            "DetectorInitializerModule ../configuration/detector.cfg\n"
            "ParticleGunModule ../configuration/particleGun_Electron.cfg\n"
            "ParticleGunModule ../configuration/particleGun_Kaon.cfg\n"
            "ParticlePrinterModule\n"
        )
        parsingResult = parse_module_sequence(testConfig)
        self.assertEqual(len(parsingResult), 4)
        for moduleSpecification in parsingResult:
            self.assertIsInstance(moduleSpecification, ModuleFactory)
            
        self.assertEqual(parsingResult[0]._module_name, "DetectorInitializerModule")
        self.assertEqual(parsingResult[0]._path_to_configuration_file, "../configuration/detector.cfg")
        self.assertEqual(parsingResult[1]._module_name, "ParticleGunModule")
        self.assertEqual(parsingResult[1]._path_to_configuration_file, "../configuration/particleGun_Electron.cfg")
        self.assertEqual(parsingResult[2]._module_name, "ParticleGunModule")
        self.assertEqual(parsingResult[2]._path_to_configuration_file, "../configuration/particleGun_Kaon.cfg")
        self.assertEqual(parsingResult[3]._module_name, "ParticlePrinterModule")
        self.assertEqual(parsingResult[3]._path_to_configuration_file, None)
        
            
            