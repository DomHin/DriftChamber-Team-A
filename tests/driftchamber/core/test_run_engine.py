# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import unittest

from driftchamber.core.run_engine import RunEngine
from driftchamber.modules.HelloWorldModule import HelloWorld
from driftchamber.modules.ByeByeWorldModule import ByeByeWorld
from testfixtures import LogCapture


class RunEngineTest(unittest.TestCase):
    """
    Test class for the RunEngine class
    """

    def test_add_module(self):
        runEngine = RunEngine(None, 20)
        module = HelloWorld()
        runEngine.add_module(module)
        self.assertListEqual(runEngine._modules, [module])
        module2 = HelloWorld()
        runEngine.add_module(module2)
        self.assertListEqual(runEngine._modules, [module, module2])
        

    def test_run_failcase(self):
            runEngine = RunEngine(None, 20.5)
            self.assertRaises(ValueError, runEngine.run)
            

    def test_run(self):
        with LogCapture() as logCapture:
            runEngine = RunEngine(None, 2)
            runEngine.add_module(HelloWorld())
            runEngine.add_module(ByeByeWorld())
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


