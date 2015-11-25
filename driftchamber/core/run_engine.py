__author__ = 'Patrick Schreiber'

from driftchamber.core.datastore import DataStore, ObjectLifetime
from driftchamber.data.detector import Detector
import logging

class RunEngine(object):

    def __init__(self, p_nEvent, p_moduleList, p_driftChamber = None, detector_config = None):
        self._datastore = DataStore()
        self._driftChamber = p_driftChamber
        self._modules = p_moduleList
        self._nEvent = p_nEvent
        self._detector_config = detector_config
        self.detector = None
        self.detector = Detector(self._detector_config['Detector_width'],
                                 self._detector_config['Detector_superlayers'],
                                 self._detector_config['Detector_layers'])

        self._datastore.put('Detector', self.detector, ObjectLifetime.Application)
        self.log_configuration()

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

        if self.detector:
            self.detector.print()
            # self.detector.show()

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

        if self.detector:
            self.detector.show()

    def log_configuration(self):
        logging.info("RunEngine configuration:")
        logging.info("--------------------------------------------------------------------")
        logging.info("modules:")
        for module in self._modules:
            logging.info(str(module.index) + "\t" + str(module.__class__))
        logging.info("detector:")
        logging.info("superlayers:\t" + str(self.detector.superlayers))
        logging.info("layers:\t" + str(self.detector.layer_info))
        logging.info("width:\t" + str(self.detector.width))
        logging.info("--------------------------------------------------------------------")
