__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.datastore import ObjectLifetime

class RunEngineInInconsistentState(Exception):
    """
    Indicates that the begin(), end(), or event() methods of the modules were called in a wrong order.
    """
    pass

class RunEngine(object):
    """
    The run engine.
    
    It calls the begin()-methods of modules, 
    then the event()-methods multiple times and 
    finally the end()-methods.
    
    This can either be done using the step-by-step interface:
    call_all_begin_methods()
    call_next_event_methods() must be called multiple times
    clear_event_based_storage()
    call_all_end_methods()
    
    or
    
    the run-method() which does all that at once.
    
    Using the interface inappropriately will raise an exception.
    """
    def __init__(self, 
                 p_module_list, 
                 p_data_store):
        """
        Ctor.
        
        :param: p_module_list   list of the modules
        :param: p_data_store    the data store
        """
        self._datastore = p_data_store
        self._nEvent = self._datastore.get('nEvent')
        if self._nEvent is None or not isinstance(self._nEvent, int):
            raise ValueError(
                ("Amount of events not specified or specified in a wrong data type. "
                 "Integer expected."))
        self._modules = p_module_list
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
        Calls the event method ONCE per module. Does not clear the event based storage.
        This is an intended behavior, because if multiple run engines (root and sub run engines) 
        work with the same data only the root run engine should reset the data)
        '''
        self._events_called += 1
        if not self._begins_called or self._events_called > self._nEvent:
            raise RunEngineInInconsistentState()
        for module in self._modules:
            module.event(self._datastore)
            
            
    def clear_event_based_storage(self):
        self._datastore.clear(ObjectLifetime.Event)
            
        
    def call_all_end_methods(self):
        if not self._begins_called or (self._events_called is not self._nEvent) or self._ends_called:
            raise RunEngineInInconsistentState()
        self._ends_called = True
        for module in self._modules:
            module.end(self._datastore)

    def run(self):
        """
        Execute all registered modules
        This runs the ``begin`` method of each module, 
        then runs the ``event`` method of each module nEvent times.
        The events are processed alternating.
        (e.g. module 1 event 1, module 2 event 1, module 1 event 2, module 2 event 2, ...)
        At the end it runs the ``end`` method of every module.
        """
        if self._begins_called:
            raise RunEngineInInconsistentState()
        self.call_all_begin_methods()
        for eventIndex in range(self._nEvent):
            self._datastore.put('current_event_index', eventIndex, ObjectLifetime.Event)
            self.call_next_event_methods()
            self.clear_event_based_storage()
        self.call_all_end_methods()
        

    def log_configuration(self):
        """
        Logs the class names of the registered modules.
        """
        logging.info("Registered modules in the run engine:")
        for module in self._modules:
            logging.info("\t" + str(module.__class__))
