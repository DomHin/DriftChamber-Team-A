__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.datastore import ObjectLifetime

class RunEngineInInconsistentState(Exception):
    """
    Exception which gets raised if an object with the
    requested lifetime does not exist in the data store
    """
    pass

class RunEngine(object):

    def __init__(self, p_moduleList, p_dataStore):
        self._datastore = p_dataStore
        self._nEvent = self._datastore.get('nEvent')
        if self._nEvent is None or not isinstance(self._nEvent, int):
            raise ValueError(
                ("Amount of events not specified or specified in a wrong data type. "
                 "Integer expected."))
        self._modules = p_moduleList
        self._begins_called = False;
        self._events_called = 0;
        self._ends_called = False;
        
    def call_all_begin_methods(self):
        if self._begins_called:
            raise RunEngineInInconsistentState()
        self._begins_called = True
        for module in self._modules:
            module.begin(self._datastore)
            
            
    def call_next_event_methods(self):
        '''
        Calls the event method ONE time per module. Does not clear the event based storage
        '''
        if not self._begins_called:
            raise RunEngineInInconsistentState()
        self._events_called += 1
        for module in self._modules:
            module.event(self._datastore)
            
        
    def call_all_end_methods(self):
        if not self._begins_called or (self._events_called is not self._nEvent) or self._ends_called:
            raise RunEngineInInconsistentState()
        self._ends_called = True
        for module in self._modules:
            module.end(self._datastore)

    def run(self):
        """
        Execute all registered modules
        This runs the ``begin`` method of every module, 
        then runs every modules ``event`` function nEvent times.
        The events are processed alternating.
        (e.g. module 1 event 1, module 2 event 1, module 1 event 2, module 2 event 2, ...)
        At the end it runs the ``end`` method of every module.
        :return:
        """
        self.call_all_begin_methods()
        for eventIndex in range(self._nEvent):
            self._datastore.put('CurrentEvent', eventIndex, ObjectLifetime.Event)
            self.call_next_event_methods()
            self._datastore.clear(ObjectLifetime.Event)
        self.call_all_end_methods()
        

    def log_configuration(self):
        logging.info("Registered modules in the run engine:")
        for module in self._modules:
            logging.info("\t" + str(module.__class__))
