__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module

class ByeByeWorld(Module):

    def __init__(self):
        self._event_nr = 1

    def begin(self, datastore):
        logging.info('Module ByeByeWorld before event processing')

    def event(self, datastore):
        logging.info('Module ByeByeWorld processing event #%d', 
                     self._event_nr)
        self._event_nr += 1

    def end(self, datastore):
        logging.info('Module ByeByeWorld after event processing')
