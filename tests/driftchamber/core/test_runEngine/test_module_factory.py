
import unittest
import os

from driftchamber.core.RunEngineFactory import ModuleFactory
from tests.driftchamber.core.test_runEngine.TestModule.TestModule import Test
from driftchamber.core.configuration.configuration import Configuration



class ModuleFactoryTest(unittest.TestCase):
    """
    Test class for the ModuleFactory class
    """
    
    def setUp(self):
        self.pathToTest = os.path.dirname(os.path.abspath(__file__))
        self.pathToModules = self.pathToTest+"/"
        self.pathToModules_py = 'tests.driftchamber.core.test_runEngine.'
        self.pathToDefaultTestConfigFile = self.pathToTest + '/test.cfg'

    def test_run(self):
        moduleFactory = ModuleFactory('TestModule', 
                                      self.pathToDefaultTestConfigFile,
                                      self.pathToModules,
                                      self.pathToModules_py)
        self.assertIsInstance(moduleFactory.get_module_instance(), Test)
        self.assertIsInstance(moduleFactory.get_module_configuration(), Configuration)