import logging
from driftchamber.core.module import Module

class ByeByeWorld(Module):

    def __init__(self):
        self._event = 1

    def event(self, datastore):
        logging.info('Module ByeByeWorld processing event #%d', self._event)
        self._event += 1
