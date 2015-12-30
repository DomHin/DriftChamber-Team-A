from numpy import array
from driftchamber.core.module import Module
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.data.detector import Detector, SuperLayer, Layer, Cell


class DetectorGeometry(Module):

    def __init__(self, **kwargs):
        self._superlayers = kwargs.get('superlayers')
        self._layers = kwargs.get('layers')
        self._cells = kwargs.get('layer_cells')

    def begin(self, datastore):
        detector = self._create_detector()

        datastore.put('detector', detector, ObjectLifetime.Application)

    def _create_detector(self):
        superlayers = []
        superlayer_y_pos = 0

        for layer_count in self._layers:
            superlayer = self._create_superlayer(layer_count,
                                                 superlayer_y_pos)
            superlayers.append(superlayer)

            superlayer_y_pos += layer_count

        return Detector(superlayers)

    def _create_superlayer(self, layer_count, y_pos):
        layers = []
        layer_y_pos = y_pos

        for _ in range(layer_count):
            cells = self._create_layer_cells(layer_y_pos)
            layer = Layer(cells)
            layers.append(layer)

            layer_y_pos += 1

        return SuperLayer(layers)

    def _create_layer_cells(self, layer_y_pos):
        cells = []

        for x_pos in range(self._cells):
            position = array([x_pos, layer_y_pos])
            cell = Cell(position)

            cells.append(cell)

        return cells
