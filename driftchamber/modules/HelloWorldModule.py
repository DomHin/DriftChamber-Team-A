__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module


class HelloWorld(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'HelloWorld'")
        self.number_of_events = 0

    def event(self, datastore):
        self.number_of_events += 1
        logging.info("Number of previous events in module 'HelloWorld': " + str(self.number_of_events))

    def end(self, datastore):
        logging.info("End of module 'HelloWorld'")

