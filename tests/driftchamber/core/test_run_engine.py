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
    def setUp(self):
        self.run_engine = RunEngine()

    def test_set_events(self):
        expected = 20
        self.run_engine.set_events(expected)
        result = self.run_engine.eventCount
        self.assertEqual(result, expected)

    def test_add_module(self):
        module = HelloWorld()
        self.run_engine.add_module(module)
        self.assertListEqual(self.run_engine._modules, [module])
        module2 = HelloWorld()
        self.run_engine.add_module(module2)
        self.assertListEqual(self.run_engine._modules, [module, module2])

    def test_run_failcase(self):
        with LogCapture() as l:
            self.run_engine.run()
            self.run_engine.set_events(1.2)
            self.run_engine.run()
            l.check(
                    ('root', 'ERROR', 'No number of Events or no integer specified.'),
                    ('root', 'ERROR', 'No number of Events or no integer specified.')
            )

    def test_run(self):
        with LogCapture() as l:
            self.run_engine.add_module(HelloWorld())
            self.run_engine.add_module(ByeByeWorld())
            self.run_engine.set_events(2)
            self.run_engine.run()
            l.check(
                    ('root', 'INFO', 'Begin of Simulation of HelloWorld'),
                    ('root', 'INFO', 'Begin of Simulation of ByeByeWorld'),
                    ('root', 'INFO', 'Number of previous Events in Hello: 1'),
                    ('root', 'INFO', 'Number of previous Events in ByeBye: 1'),
                    ('root', 'INFO', 'Number of previous Events in Hello: 2'),
                    ('root', 'INFO', 'Number of previous Events in ByeBye: 2'),
                    ('root', 'INFO', 'End of Simulation of HelloWorld'),
                    ('root', 'INFO', 'End of Simulation of ByeByeWorld')
            )


