__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module

class ByeByeWorld(Module):

    def begin(self, datastore):
        self.number_of_events = 0
        logging.info("Begin of module 'ByeByeWorld'")

    def event(self, datastore):
        self.number_of_events += 1
        logging.info("Number of previous events in module 'ByeByeWorld': " + str(self.number_of_events))

    def end(self, datastore):
        logging.info("End of module 'ByeByeWorld'")

