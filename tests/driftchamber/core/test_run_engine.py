# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import unittest
from testfixtures import LogCapture

from driftchamber.core.run_engine import RunEngine
from driftchamber.modules.HelloWorldModule import HelloWorld
from driftchamber.modules.ByeByeWorldModule import ByeByeWorld


class RunEngineTest(unittest.TestCase):
    """
    Test class for the RunEngine class
    """       

    def test_run_failcase(self):
            runEngine = RunEngine(20.5, [], None)
            self.assertRaises(ValueError, runEngine.run)
            

    def test_run(self):
        with LogCapture() as logCapture:
            runEngine = RunEngine(2, [HelloWorld(), ByeByeWorld()], None)
            runEngine.run()
            logCapture.check(
                    ('root', 'INFO', 'Begin of Simulation of HelloWorld'),
                    ('root', 'INFO', 'Begin of Simulation of ByeByeWorld'),
                    ('root', 'INFO', 'Number of previous Events in Hello: 1'),
                    ('root', 'INFO', 'Number of previous Events in ByeBye: 1'),
                    ('root', 'INFO', 'Number of previous Events in Hello: 2'),
                    ('root', 'INFO', 'Number of previous Events in ByeBye: 2'),
                    ('root', 'INFO', 'End of Simulation of HelloWorld'),
                    ('root', 'INFO', 'End of Simulation of ByeByeWorld')
            )


