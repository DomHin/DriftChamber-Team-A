# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import unittest
from testfixtures import LogCapture
from driftchamber.modules.HelloWorldModule import HelloWorld


class HelloWorldTest(unittest.TestCase):
    """
    Test class for the HelloWorld class
    """
    def setUp(self):
        self.module = HelloWorld()

    def test_begin(self):
        with LogCapture() as l:
            self.module.begin(None)

            l.check(
                    ('root', 'INFO', 'Begin of Simulation of HelloWorld')
            )

    def test_event(self):
        with LogCapture() as l:
            self.module.event(None)
            self.module.event(None)

            l.check(
                    ('root', 'INFO', 'Number of previous Events in Hello: 1'),
                    ('root', 'INFO', 'Number of previous Events in Hello: 2')
            )

    def test_end(self):
        with LogCapture() as l:
            self.module.end(None)

            l.check(
                    ('root', 'INFO', 'End of Simulation of HelloWorld')
            )

