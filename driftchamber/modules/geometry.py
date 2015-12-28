from driftchamber.core.module import Module
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.data.detector import Detector, SuperLayer, Layer, Cell


class DetectorGeometry(Module):

    def __init__(self, **kwargs):
        self._superlayers = kwargs.get('superlayers')
        self._layers = kwargs.get('layers')
        self._cells = kwargs.get('cells')

    def begin(self, datastore):
        superlayers = self._create_superlayers()
        detector = Detector(superlayers)

        datastore.put('detector', detector, ObjectLifetime.Application)

    def _create_superlayers(self):
        return [SuperLayer(self._create_layers(count))
                for count in self._layers]

    def _create_layers(self, count):
        return [Layer(self._create_cells()) for _ in range(count)]

    def _create_cells(self):
        return [Cell() for _ in range(self._cells)]
