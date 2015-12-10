import unittest
import os

from driftchamber.core.config.config import Configuration
from driftchamber.core.datastore import DataStore, ObjectLifetime
from driftchamber.modules.detectorinitializer.config_specification import configuration_specification
from driftchamber.modules.detectorinitializer.detector_initializer import DetectorInitializer

class TestDetectorInitializerModule(unittest.TestCase):
    """
    Test class for the DetectorInitializerModule class
    """
    
    def setUp(self):
        self.pathToConfgiFiles = os.path.dirname(os.path.abspath(__file__))
        self.path_to_default_test_config_file = self.pathToConfgiFiles + '/detector.cfg'

    def test_run(self):
        configuration = Configuration(self.path_to_default_test_config_file, configuration_specification)
        dataStore = DataStore()
        module = DetectorInitializer()
        dataStore.put(module, configuration, ObjectLifetime.Application)
        module.begin(dataStore)
        # now, there must be a detector present
        detector = dataStore.get('Detector')
        self.assertEqual(detector.width, 100)
        self.assertEqual(detector.nSuperLayers, 11)
        self.assertEqual(detector.nLayersList, [1, 5, 5, 2, 6, 6, 2, 7, 5, 7, 8])
        