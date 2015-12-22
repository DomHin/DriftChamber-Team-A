from driftchamber.core.datastore import DataStore
from driftchamber.core.module import Module

class RunEngine(object):
    
    def __init__(self, events = 0):
        self._modules = []
        self._events = events
        self._datastore = DataStore()
        
    @property
    def events(self):
        return self._events
        
    @events.setter
    def events(self, value):
        self._events = value
    
    def add_module(self, module):
        if not isinstance(module, Module):
            raise TypeError('This is not a module.')
        
        self._modules.append(module)
    
    def execute(self):
        for m in self._modules:
            m.begin(self._datastore)
        
        for _ in range(self.events):
            for m in self._modules:
                m.event(self._datastore)
            
        for m in self._modules:
            m.end(self._datastore)