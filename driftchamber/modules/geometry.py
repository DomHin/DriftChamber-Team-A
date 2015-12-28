from driftchamber.core.module import Module
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.data.detector import Detector, SuperLayer, Layer, Cell


class DetectorGeometry(Module):

    def __init__(self, **kwargs):
        self._superlayer_counts = kwargs.get('superlayers')
        self._layer_counts = kwargs.get('layers')
        self._cells_per_layer = kwargs.get('cells')

    def begin(self, datastore):
        detector = Detector(self._superlayers())

        datastore.put('detector', detector, ObjectLifetime.Application)

    def _superlayers(self):
        return [SuperLayer(self._layers(count)) 
                for count in self._layer_counts]

    def _layers(self, count):
        return [Layer(self._cells()) for _ in range(count)]

    def _cells(self):
        return [Cell() for _ in range(self._cells_per_layer)]
