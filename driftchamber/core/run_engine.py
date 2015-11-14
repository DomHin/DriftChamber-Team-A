__author__ = 'Patrick Schreiber'

from driftchamber.core.datastore import DataStore, ObjectLifetime
import logging

class RunEngine(object):

    def __init__(self):
        self._modules = []
        self.eventCount = None
        self.datastore = DataStore()

    def set_events(self, event_count):
        """
        Specify the number of events to run
        :param int event_count: The number of events to run
        """
        self.eventCount = event_count

    def add_module(self, module):
        """
        Add/Register a module to run it during simulation
        :param object module: A python object representing the module to run
        """
        self._modules.append(module)

    def run(self):
        """
        Execute all registered modules
        This runs the ``begin`` method of every module, then runs every modules ``event`` function event_count
        (This is the number specified via set_events) times. The events are run alternating.
        (e.g. Module 1 event 1, Module 2 event 1, Module 1 event 2, Module 2 event 2 ...)
        At the end it runs the ``end`` method of every module.
        :return:
        """
        if self.eventCount is None or not isinstance(self.eventCount, int):
            logging.error("No number of Events or no integer specified.")
            return

        # Run begin functions of every module
        for module in self._modules:
            module.begin(self.datastore)

        # Evaluate Events of every modules eventCount times
        for n in range(self.eventCount):
            for module in self._modules:
                module.event(self.datastore)
            # clear event based storage.
            self.datastore.clear(ObjectLifetime.Event)

        # Run end function of every module
        for module in self._modules:
            module.end(self.datastore)
