import unittest
from driftchamber.core.run_engine import RunEngine
from driftchamber.core.datastore import ObjectLifetime, NotFoundInDataStore

class RunEngineTest(unittest.TestCase):
    
    def test_datastore_object_lifetimes(self):
        engine = RunEngine()
        engine.events = 1
        engine._datastore.put('item1', {}, ObjectLifetime.Application)
        engine._datastore.put('item2', {}, ObjectLifetime.Event)
        engine.execute()
        
        with self.assertRaises(NotFoundInDataStore):
            engine._datastore.get('item2')
            
        try:
            engine._datastore.get('item1')
        except NotFoundInDataStore:
            self.fail()