# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import unittest

from driftchamber.core.run_engine import RunEngine, RunEngineInInconsistentState
from driftchamber.core.datastore import DataStore, ObjectLifetime, NotFoundInDataStore
from driftchamber.core.module import Module
from driftchamber.tests.core.test_run_engine.TestModule.TestModule import Test
        
class TestObjectLifeTimeModule(Module):

    def __init__(self, p_callFromEventMethod):
        self.data_eventLifeTime = None
        self.data_ApplicationLifeTime = None
        self.callFromEventMethod = p_callFromEventMethod
    
    def begin(self, data_store):
        data_store.put('ApplicationLifetime', self.data_ApplicationLifeTime, ObjectLifetime.Application)

    def event(self, data_store):
        self.callFromEventMethod()
        data_store.put('EventLifetime', self.data_eventLifeTime, ObjectLifetime.Event)

    def end(self, data_store):
        pass
    
class TestOrderOfExcecutionModule(Module):
    def __init__(self, pIndex, p_order_begin_list, p_order_event_list, p_order_end_list):
        self._index = pIndex
        self._order_begin_list = p_order_begin_list
        self._order_event_list = p_order_event_list
        self._order_end_list = p_order_end_list
    
    def begin(self, data_store):
        self._order_begin_list.append(self._index)

    def event(self, data_store):
        self._order_event_list.append(self._index)

    def end(self, data_store):
        self._order_end_list.append(self._index)
        
class run_engineTest(unittest.TestCase):
    """
    Test class for the run_engine class
    """          

    def test_run(self):
        test_module1 = Test()
        test_module2 = Test()
        data_store = DataStore()
        data_store.put('nEvent', 100)
        
        self.assertEqual(test_module1.beginCalled, 0)
        self.assertEqual(test_module1.eventCalled, 0)
        self.assertEqual(test_module1.endCalled, 0)
        
        self.assertEqual(test_module2.beginCalled, 0)
        self.assertEqual(test_module2.eventCalled, 0)
        self.assertEqual(test_module2.endCalled, 0)

        run_engine = RunEngine([test_module1, test_module2], data_store)
        run_engine.run()
        
        self.assertEqual(test_module1.beginCalled, 1)
        self.assertEqual(test_module1.eventCalled, 100)
        self.assertEqual(test_module1.endCalled, 1)
        
        self.assertEqual(test_module2.beginCalled, 1)
        self.assertEqual(test_module2.eventCalled, 100)
        self.assertEqual(test_module2.endCalled, 1)
        
    def test_objectLifeTime(self):
        data_store = DataStore()
        self_wrapper = self
        test_module = TestObjectLifeTimeModule(lambda: self_wrapper.assertRaises(NotFoundInDataStore, data_store.get, 'EventLifetime'))
        data_store.put('nEvent', 2)
        run_engine = RunEngine([test_module], data_store)
        run_engine.run()
        data_store.get('ApplicationLifetime')
        
    def test_order_of_execution(self):
        order_begin_list = []
        order_event_list = []
        order_end_list = []
        test_module0 = TestOrderOfExcecutionModule(0, order_begin_list, order_event_list, order_end_list)
        test_module1 = TestOrderOfExcecutionModule(1, order_begin_list, order_event_list, order_end_list)
        test_module2 = TestOrderOfExcecutionModule(2, order_begin_list, order_event_list, order_end_list)
        data_store = DataStore()
        data_store.put('nEvent', 3)
        
        run_engine = RunEngine([test_module0, test_module1, test_module2], data_store)
        run_engine.run()
        self.assertEqual(order_begin_list, [0, 1, 2])
        self.assertEqual(order_event_list, [0, 1, 2, 0, 1, 2, 0, 1, 2,])
        self.assertEqual(order_end_list, [0, 1, 2])
        
    def test_impossibility_to_get_run_engine_in_invalid_state(self):
        test_module1 = Test()
        test_module2 = Test()
        data_store = DataStore()
        data_store.put('nEvent', 2)
        run_engine = RunEngine([test_module1, test_module2], data_store)
        self.assertRaises(RunEngineInInconsistentState, run_engine.call_next_event_methods)
        
        test_module1 = Test()
        test_module2 = Test()
        data_store = DataStore()
        data_store.put('nEvent', 2)
        run_engine = RunEngine([test_module1, test_module2], data_store)
        self.assertRaises(RunEngineInInconsistentState, run_engine.call_all_end_methods)
        
        test_module1 = Test()
        test_module2 = Test()
        data_store = DataStore()
        data_store.put('nEvent', 2)
        run_engine = RunEngine([test_module1, test_module2], data_store)
        run_engine.call_all_begin_methods()
        self.assertRaises(RunEngineInInconsistentState, run_engine.call_all_begin_methods)
        
        test_module1 = Test()
        test_module2 = Test()
        data_store = DataStore()
        data_store.put('nEvent', 2)
        run_engine = RunEngine([test_module1, test_module2], data_store)
        run_engine.call_all_begin_methods()
        run_engine.call_next_event_methods()
        run_engine.clear_event_based_storage()
        run_engine.call_next_event_methods()
        run_engine.clear_event_based_storage()
        # can not call call_next_event_methods() method more often than nEvent times
        self.assertRaises(RunEngineInInconsistentState, run_engine.call_next_event_methods)
        
        test_module1 = Test()
        test_module2 = Test()
        data_store = DataStore()
        data_store.put('nEvent', 2)
        run_engine = RunEngine([test_module1, test_module2], data_store)
        run_engine.call_all_begin_methods()
        run_engine.call_next_event_methods()
        run_engine.clear_event_based_storage()
        run_engine.call_next_event_methods()
        run_engine.clear_event_based_storage()
        run_engine.call_all_end_methods()
        self.assertRaises(RunEngineInInconsistentState, run_engine.call_all_end_methods)

