__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.datastore import ObjectLifetime


class RunEngine(object):

    def __init__(self, p_moduleList, p_dataStore):
        self._datastore = p_dataStore
        self._nEvent = self._datastore.get('nEvent')
        self._modules = p_moduleList

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
            self._datastore.put('CurrentEvent', n)
            for module in self._modules:
                module.event(self._datastore)
            # clear event based storage.
            self._datastore.clear(ObjectLifetime.Event)

        for module in self._modules:
            module.end(self._datastore)

    def log_configuration(self):
        logging.info("Registered modules in the run engine:")
        for module in self._modules:
            logging.info("\t" + str(module.__class__))
