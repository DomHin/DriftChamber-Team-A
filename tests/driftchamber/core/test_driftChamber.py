# -*- coding: utf-8 -*-
"""
@author: Fabian Leven
"""

import unittest
import driftchamber.drift_chamber as mainModule
import os

class DriftChamberTest(unittest.TestCase):
    """
    Test class for the DriftChamber class
    """
    
    def setUp(self):
        self.pathToConfgiFiles = os.path.dirname(os.path.abspath(__file__))
        self.pathToConfigFile = self.pathToConfgiFiles+'/../../../configurations/test_config_allOptions.cfg'

    def test_main(self):
        try:
            mainModule.main(['--config', self.pathToConfigFile, '--General_nEvent', '1'])
        except:
            self.fail("Calling the main module should not throw an exception.")
            
            
    def test_configurationIsNotNone(self):
        driftChamber = mainModule.DriftChamber(['--config', self.pathToConfigFile])
        self.assertIsNotNone(driftChamber.getConfiguration())