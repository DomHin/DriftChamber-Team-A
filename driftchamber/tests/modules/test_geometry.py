from unittest.case import TestCase
from driftchamber.core.datastore import DataStore
from driftchamber.modules.geometry import DetectorGeometry


class DetectorGeometryTest(TestCase):

    def setUp(self):
        datastore = DataStore()
        geometry = DetectorGeometry(superlayers=4,
                                    layers=[4, 2, 5, 1],
                                    layer_cells=5)
        geometry.begin(datastore)

        self.detector = datastore.get('detector')

    def test_dimensions(self):
        self.assertEqual(self.detector.width, 5)
        self.assertEqual(self.detector.height, 12)

    def test_layer_counts(self):
        self.assertEqual(len(self.detector.superlayers), 4)
        self.assertEqual(self.detector.superlayers[0].layer_count, 4)
        self.assertEqual(self.detector.superlayers[1].layer_count, 2)
        self.assertEqual(self.detector.superlayers[2].layer_count, 5)
        self.assertEqual(self.detector.superlayers[3].layer_count, 1)

    def test_cell_positions(self):
        cell_y_pos = 0

        for superlayer in self.detector.superlayers:
            for layer in superlayer.layers:
                for index, cell in enumerate(layer.cells):
                    position = cell.position

                    self.assertEqual(index, position[0])
                    self.assertEqual(cell_y_pos, position[1])

                cell_y_pos += 1
