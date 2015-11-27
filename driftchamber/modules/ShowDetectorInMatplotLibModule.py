import logging
import matplotlib.pyplot as plt

from driftchamber.core.module import Module


class ShowDetectorInMatplotLib(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'ShowDetectorInMatplotLib'")
        self._detector = datastore.get('Detector')


    def event(self, datastore):
        pass

    def end(self, datastore):
        self._showDetecor()
        logging.info("End of module 'ShowDetectorInMatplotLib'")
        

    def _showDetecor(self):
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'black', 'magenta', 'purple', 'lightblue', 'grey']
        for idx, sl in enumerate(self._detector.detector):
            for layer in sl.layers:
                for cell in layer.cells:
                    fillstyle = 'full' if cell.is_triggered() else 'none'
                    plt.plot(cell.pos[0], cell.pos[1], marker='s', fillstyle=fillstyle, color=colors[idx % len(colors)])
        plt.ylim(-0.5, self._detector.height-0.5)
        plt.show()
