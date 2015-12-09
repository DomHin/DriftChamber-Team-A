__author__ = 'Fabian Leven'

import logging

from driftchamber.core.module import Module
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.data.detector import Detector

class DetectorInitializer(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'DetectorInitializer'")
        configuration = datastore.get(self)
        width = configuration['Detector_width']
        nSuperLayers = configuration['Detector_nSuperLayers']
        nLayersList = configuration['Detector_nLayersList']
        self._detector = Detector(width, nSuperLayers, nLayersList)
        datastore.put(
            'Detector',
            self._detector,
            ObjectLifetime.Application)
        self._logInfo()

    def event(self, datastore):
        pass

    def end(self, datastore):
        logging.info("End of module 'DetectorInitializer'")
    
    def _logInfo(self):
        logging.info((
            "Detector initialized with:\n"
            "\t width: " + str(self._detector.width) + "\n"
            "\t amount of super layers: " + str(self._detector.nSuperLayers) + "\n"
            "\t amount of sup layers: " + str(self._detector.nLayersList)
            ))






