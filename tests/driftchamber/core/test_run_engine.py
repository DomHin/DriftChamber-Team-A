# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import unittest

from testfixtures import LogCapture

from driftchamber.core.run_engine import RunEngine
from driftchamber.modules.ByeByeWorldModule import ByeByeWorld
from driftchamber.modules.HelloWorldModule import HelloWorld


class RunEngineTest(unittest.TestCase):
    """
    Test class for the RunEngine class
    """       

    def test_run_failcase(self):
            runEngine = RunEngine(20.5, [], {"Detector_superlayers": 0, "Detector_layers": [], "Detector_width": 0})
            self.assertRaises(ValueError, runEngine.run)
            

    def test_run(self):
        with LogCapture() as logCapture:
            runEngine = RunEngine(2, [HelloWorld([0]), ByeByeWorld([0])], {"Detector_superlayers": 1, "Detector_layers": [1], "Detector_width": 1})
            runEngine.run()
            logCapture.check(
                             ('root', 'INFO', 'Begin of Simulation of HelloWorld'),
                             ('root', 'INFO', 'Begin of Simulation of ByeByeWorld'),
                             ('root', 'INFO', 'Number of previous Events in Hello: 1'),
                             ('root', 'INFO', 'Number of previous Events in ByeBye: 1'),
                             ('root', 'INFO', 'Number of previous Events in Hello: 2'),
                             ('root', 'INFO', 'Number of previous Events in ByeBye: 2'),
                             ('root', 'INFO', 'End of Simulation of HelloWorld'),
                             ('root', 'INFO', 'End of Simulation of ByeByeWorld'))


