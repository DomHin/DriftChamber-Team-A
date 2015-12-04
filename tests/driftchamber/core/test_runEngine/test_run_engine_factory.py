
import unittest
import os

from driftchamber.core.RunEngineFactory import ModuleFactory, RunEngineFactory
from driftchamber.core.run_engine import RunEngine
from driftchamber.core.datastore import DataStore



class RunEngineFactoryTest(unittest.TestCase):
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
        dataStore = DataStore()
        dataStore.put('nEvent', 2)
        self.assertIsInstance(RunEngineFactory([moduleFactory], dataStore).get_run_engine(), RunEngine)