import logging
from driftchamber.core.module import Module

class HelloWorld(Module):

    def __init__(self):
        self._event = 1
        
    def event(self, datastore):
        logging.info('Module HelloWorld processing event #%d', self._event)
        self._event += 1
