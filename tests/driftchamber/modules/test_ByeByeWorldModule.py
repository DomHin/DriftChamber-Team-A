# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import unittest

from testfixtures import LogCapture

from driftchamber.modules.ByeByeWorldModule import ByeByeWorld


class ByeByeWorldTest(unittest.TestCase):
    """
    Test class for the ByeByeWorld class
    """
    def setUp(self):
        self.module = ByeByeWorld([0])

    def test_begin(self):
        with LogCapture() as l:
            self.module.begin(None)

            l.check(
                    ('root', 'INFO', 'Begin of Simulation of ByeByeWorld')
            )

    def test_event(self):
        with LogCapture() as l:
            self.module.event(None)
            self.module.event(None)

            l.check(
                    ('root', 'INFO', 'Number of previous Events in ByeBye: 1'),
                    ('root', 'INFO', 'Number of previous Events in ByeBye: 2')
            )

    def test_end(self):
        with LogCapture() as l:
            self.module.end(None)

            l.check(
                    ('root', 'INFO', 'End of Simulation of ByeByeWorld')
            )

