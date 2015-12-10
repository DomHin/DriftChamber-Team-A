__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module

class HelloWorld(Module):

    def begin(self, datastore):
        logging.info('Module HelloWorld before event processing')

    def event(self, datastore):
        logging.info('Module HelloWorld during event processing')

    def end(self, datastore):
        logging.info('Module HelloWorld after event processing')
