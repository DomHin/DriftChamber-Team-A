#! /usr/bin/env python3.4

import unittest
import os

from driftchamber.core.run_engine_factory import ModuleFactory, RunEngineFactory
from driftchamber.core.run_engine import RunEngine
from driftchamber.core.datastore import DataStore


class RunEngineFactoryTest(unittest.TestCase):
    """
    Test class for the ModuleFactory class.
    """
    
    def setUp(self):
        self.path_to_test = os.path.dirname(os.path.abspath(__file__))
        self.path_to_test_modules = self.path_to_test+"/"
        self.path_to_test_modules_py = 'driftchamber.tests.core.test_run_engine.'
        self.path_to_default_test_config_file = self.path_to_test + '/test.cfg'

    def test_run(self):
        moduleFactory = ModuleFactory('TestModule', 
                                      self.path_to_default_test_config_file,
                                      self.path_to_test_modules,
                                      self.path_to_test_modules_py)
        module = moduleFactory.get_module_instance()
        data_store = DataStore()
        data_store.put('nEvent', 2)
        run_engine = RunEngineFactory([moduleFactory], data_store).get_run_engine()
        self.assertIsInstance(run_engine, RunEngine)
        run_engine.run()
        self.assertEqual(module.beginCalled, 1)
        self.assertEqual(module.eventCalled, 2)
        self.assertEqual(module.endCalled, 1)