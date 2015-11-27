__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module


class ShowDetecorInConsole(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'ShowDetecorInConsole'")
        self._detector = datastore.get('Detector')

    def event(self, datastore):
        pass

    def end(self, datastore):
        self._showDetecorInConsole()
        logging.info("End of module 'ShowDetecorInConsole")

    def _showDetecorInConsole(self):
        symbols = ['o', 'x', 'O', 'X', ':', '.', 'I', '-', '#', '@']
        for index, sl in enumerate(self._detector.detector):
            for layer in sl.layers:
                for _ in layer.cells:
                    print(symbols[index % len(symbols)], end='')
                print('')
