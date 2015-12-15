__author__ = 'Patrick Schreiber'

import logging
from driftchamber.core.module import Module

class HelloWorld(Module):

    def __init__(self):
        self._event_nr = 1

    def begin(self, datastore):
        logging.info('Module HelloWorld before event processing')

    def event(self, datastore):
        logging.info('Module HelloWorld processing event #%d', self._event_nr)
        self._event_nr += 1

    def end(self, datastore):
        logging.info('Module HelloWorld after event processing')
