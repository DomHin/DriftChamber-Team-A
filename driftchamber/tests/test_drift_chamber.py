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
        self.pathToConfigFile = self.pathToConfgiFiles + '/config.cfg'

    def test_main(self):
        try:
            mainModule.main(['--config', self.pathToConfigFile])
        except:
            self.fail("Calling the main module should not throw an exception.")