__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module

class ByeByeWorld(Module):

    def begin(self, datastore):
        logging.info('Module ByeByeWorld before event processing')

    def event(self, datastore):
        logging.info('Module ByeByeWorld during event processing')

    def end(self, datastore):
        logging.info('Module ByeByeWorld after event processing')

