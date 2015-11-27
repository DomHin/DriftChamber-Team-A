# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
from driftchamber.core.module import Module

__author__ = 'elcerdo'

import unittest

from driftchamber.core.run_engine import RunEngine
from driftchamber.core.datastore import DataStore, ObjectLifetime,\
    NotFoundInDataStore

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
        
class TestObjectLifeTimeModule(Module):

    def __init__(self, p_callFromEventMethod):
        self.data_eventLifeTime = None
        self.data_ApplicationLifeTime = None
        self.callFromEventMethod = p_callFromEventMethod
    
    def begin(self, datastore):
        datastore.put('ApplicationLifetime', self.data_ApplicationLifeTime, ObjectLifetime.Application)

    def event(self, datastore):
        self.callFromEventMethod()
        datastore.put('EventLifetime', self.data_eventLifeTime, ObjectLifetime.Event)

    def end(self, datastore):
        pass
        

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
        
    def test_objectLifeTime(self):
        dataStore = DataStore()
        selfWrapper = self
        testModule = TestObjectLifeTimeModule(lambda: selfWrapper.assertRaises(NotFoundInDataStore, dataStore.get, 'EventLifetime'))
        dataStore.put('nEvent', 2)
        runEngine = RunEngine([testModule], dataStore)
        runEngine.run()
        dataStore.get('ApplicationLifetime')
        
    #todo add test for right order of execution


