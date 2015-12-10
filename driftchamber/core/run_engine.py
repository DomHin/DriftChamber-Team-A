__author__ = 'Patrick Schreiber, Genti Saliu'

from driftchamber.core.datastore import DataStore
from driftchamber.core.module import Module

class RunEngine(object):
    
    def __init__(self, nr_events = 1):
        self.__modules = []
        self.__nr_events = nr_events
        self.__datastore = DataStore()
        
    @property
    def nr_events(self, nr_events):
        self.__nr_events = nr_events
    
    def add_module(self, module):
        if not isinstance(module, Module):
            raise TypeError('This is not a module.')
        
        self.__modules.append(module)
    
    def execute(self):
        for module in self.__modules:
            module.begin(self.__datastore)
        
        for _ in range(self.__nr_events):
            for module in self.__modules:
                module.event(self.__datastore)
            
        for module in self.__modules:
            module.end(self.__datastore)