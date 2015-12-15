__author__ = 'Patrick Schreiber, Genti Saliu'

from driftchamber.core.datastore import DataStore
from driftchamber.core.module import Module

class RunEngine(object):
    
    def __init__(self, nr_events = 1):
        self._modules = []
        self._nr_events = nr_events
        self._datastore = DataStore()
        
    @property
    def nr_events(self):
        return self._nr_events
        
    @nr_events.setter
    def nr_events(self, value):
        self._nr_events = value
    
    def add_module(self, module):
        if not isinstance(module, Module):
            raise TypeError('This is not a module.')
        
        self._modules.append(module)
    
    def execute(self):
        for module in self._modules:
            module.begin(self._datastore)
        
        for _ in range(self._nr_events):
            for module in self._modules:
                module.event(self._datastore)
            
        for module in self._modules:
            module.end(self._datastore)