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
    
class TestOrderOfExcecutionModule(Module):
    def __init__(self, pIndex, p_order_begin_list, p_order_event_list, p_order_end_list):
        self._index = pIndex
        self._order_begin_list = p_order_begin_list
        self._order_event_list = p_order_event_list
        self._order_end_list = p_order_end_list
    
    def begin(self, datastore):
        self._order_begin_list.append(self._index)

    def event(self, datastore):
        self._order_event_list.append(self._index)

    def end(self, datastore):
        self._order_end_list.append(self._index)
        
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
        
    def test_order_of_execution(self):
        order_begin_list = []
        order_event_list = []
        order_end_list = []
        testModule0 = TestOrderOfExcecutionModule(0, order_begin_list, order_event_list, order_end_list)
        testModule1 = TestOrderOfExcecutionModule(1, order_begin_list, order_event_list, order_end_list)
        testModule2 = TestOrderOfExcecutionModule(2, order_begin_list, order_event_list, order_end_list)
        dataStore = DataStore()
        dataStore.put('nEvent', 3)
        
        runEngine = RunEngine([testModule0, testModule1, testModule2], dataStore)
        runEngine.run()
        self.assertEqual(order_begin_list, [0, 1, 2])
        self.assertEqual(order_event_list, [0, 1, 2, 0, 1, 2, 0, 1, 2,])
        self.assertEqual(order_end_list, [0, 1, 2])


