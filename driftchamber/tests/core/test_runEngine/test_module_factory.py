#! /usr/bin/env python3.4

import unittest
import os

from driftchamber.core.run_engine_factory import ModuleFactory
from tests.driftchamber.core.test_runEngine.TestModule.TestModule import Test
from driftchamber.core.configuration.configuration import Configuration



class ModuleFactoryTest(unittest.TestCase):
    """
    Test class for the ModuleFactory class
    """
    
    def setUp(self):
        self.path_to_test = os.path.dirname(os.path.abspath(__file__))
        self.path_to_test_modules = self.path_to_test+"/"
        self.path_to_test_modules_py = 'tests.driftchamber.core.test_runEngine.'
        self.path_to_default_test_config_file = self.path_to_test + '/test.cfg'

    def test_run(self):
        moduleFactory = ModuleFactory('TestModule', 
                                      self.path_to_default_test_config_file,
                                      self.path_to_test_modules,
                                      self.path_to_test_modules_py)
        self.assertIsInstance(moduleFactory.get_module_instance(), Test)
        self.assertIsInstance(moduleFactory.get_module_configuration(), Configuration)