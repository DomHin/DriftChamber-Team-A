# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
from driftchamber.core.module import Module

__author__ = 'elcerdo'

import unittest

from driftchamber.core.run_engine import RunEngine
from driftchamber.core.datastore import DataStore

class TestModule(Module):
    
    def __init__(self):
        self.beginCalled = 0
        self.eventCalled = 0
        self.endCalled = 0
    
    def begin(self, datastore):
        self.beginCalled += 1

    def event(self, datastore):
        self.eventCalled += 1

    def end(self, datastore):
        self.endCalled += 1


class RunEngineTest(unittest.TestCase):
    """
    Test class for the RunEngine class
    """          

    def test_run(self):
        testModule1 = TestModule()
        testModule2 = TestModule()
        dataStore = DataStore()
        dataStore.put('nEvent', 100)
        
        self.assertEqual(testModule1.beginCalled, 0)
        self.assertEqual(testModule1.eventCalled, 0)
        self.assertEqual(testModule1.endCalled, 0)
        
        self.assertEqual(testModule2.beginCalled, 0)
        self.assertEqual(testModule2.eventCalled, 0)
        self.assertEqual(testModule2.endCalled, 0)

        runEngine = RunEngine([testModule1, testModule2], dataStore)
        runEngine.run()
        
        self.assertEqual(testModule1.beginCalled, 1)
        self.assertEqual(testModule1.eventCalled, 100)
        self.assertEqual(testModule1.endCalled, 1)
        
        self.assertEqual(testModule2.beginCalled, 1)
        self.assertEqual(testModule2.eventCalled, 100)
        self.assertEqual(testModule2.endCalled, 1)
        
    #todo add test for right order of execution


