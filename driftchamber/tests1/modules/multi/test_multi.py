#! /usr/bin/env python3.4

import unittest
import os

from driftchamber.tests.modules.multi.config_specification import configuration_specification
from driftchamber.core.config.config import Configuration
from driftchamber.core.datastore import DataStore, ObjectLifetime
from driftchamber.modules.multi.multi import MultiModule



class TestMultiModule(unittest.TestCase):
    """
    Test class for the MultiModuleModule class
    """    

    def setUp(self):
        self.pathToConfgiFiles = os.path.dirname(os.path.abspath(__file__))
        self.path_to_default_test_config_file = self.pathToConfgiFiles + '/multiModule_TestModules.cfg'

    def test_run(self):
        configuration = Configuration(self.path_to_default_test_config_file, configuration_specification)
        dataStore = DataStore()
        dataStore.put('nEvent', 2)
        module = MultiModule()
        dataStore.put(module, configuration, ObjectLifetime.Application)
        module.begin(dataStore)
        module.event(dataStore)
        module.event(dataStore)
        module.end(dataStore)
        