from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.module import Module
from driftchamber.data.detector import Detector, SuperLayer, Layer, Cell
from driftchamber.math import Point2D


class DetectorGeometry(Module):

    def __init__(self, **kwargs):
        self._superlayers = kwargs.get('superlayers')
        self._layers = kwargs.get('layers')
        self._cells = kwargs.get('layer_cells')

    def begin(self, datastore):
        superlayers = self._create_superlayers()
        detector = Detector(superlayers)

        datastore.put('detector', detector, ObjectLifetime.Application)

    def _create_superlayers(self):
        superlayers = []
        cell_y = 0

        for layer_count in self._layers:
            layers = []

            for _ in range(layer_count):
                cells = []

                for cell_x in range(self._cells):
                    position = Point2D(cell_x, cell_y)
                    cell = Cell(position)
                    cells.append(cell)

                cell_y += 1
                layer = Layer(cells)
                layers.append(layer)

            superlayer = SuperLayer(layers)
            superlayers.append(superlayer)

        return superlayers
