__author__ = 'Patrick Schreiber'

from driftchamber.core.datastore import DataStore, ObjectLifetime

class RunEngine(object):

    def __init__(self, driftChamper, p_nEvent):
        self._datastore = DataStore()
        self._driftChamper = driftChamper
        self._modules = []
        self._nEvent = p_nEvent
        

    def add_module(self, module):
        """
        Add/Register a module to run it during the simulation
        :param object module: A python object representing the module that shall be executed
        """
        self._modules.append(module)

    def run(self):
        """
        Execute all registered modules
        This runs the ``begin`` method of every module, then runs every modules ``event`` function nEvent times. The events are run alternating.
        (e.g. module 1 event 1, module 2 event 1, module 1 event 2, module 2 event 2, ...)
        At the end it runs the ``end`` method of every module.
        :return:
        """
        if self._nEvent is None or not isinstance(self._nEvent, int):
            raise ValueError("Amount of events not specified or specified in a wrong data type. Integer expected.")

        # Run begin functions of every module
        for module in self._modules:
            module.begin(self._datastore)

        # Evaluate Events of every modules eventCount times
        for n in range(self._nEvent):
            for module in self._modules:
                module.event(self._datastore)
            # clear event based storage.
            self._datastore.clear(ObjectLifetime.Event)

        # Run end function of every module
        for module in self._modules:
            module.end(self._datastore)
