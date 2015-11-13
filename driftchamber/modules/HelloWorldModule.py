__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module


class HelloWorld(Module):

    number_of_events = 0

    def begin(self, datastore):
        # print("Begin of Simulation of HelloWorld")
        logging.info('Begin of Simulation of HelloWorld')

    def event(self, datastore):
        self.number_of_events += 1
        # print("Number of previous Events: " + str(self.number_of_events))
        logging.info('Number of previous Events in Hello: ' + str(self.number_of_events))

    def end(self, datastore):
        # print("End of Simulation of HelloWorld")
        logging.info('End of Simulation of HelloWorld')

