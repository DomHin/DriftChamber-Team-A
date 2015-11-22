__author__ = 'Patrick Schreiber'

from driftchamber.core.datastore import DataStore, ObjectLifetime

class RunEngine(object):

    def __init__(self, p_nEvent, p_moduleList, p_driftChamper = None):
        self._datastore = DataStore()
        self._driftChamper = p_driftChamper
        self._modules = p_moduleList
        self._nEvent = p_nEvent 

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
        if self._nEvent is None or not isinstance(self._nEvent, int):
            raise ValueError(
                ("Amount of events not specified or specified in a wrong data type. "
                 "Integer expected."))

        for module in self._modules:
            module.begin(self._datastore)

        for n in range(self._nEvent):
            for module in self._modules:
                module.event(self._datastore)
            # clear event based storage.
            self._datastore.clear(ObjectLifetime.Event)
            
        for module in self._modules:
            module.end(self._datastore)