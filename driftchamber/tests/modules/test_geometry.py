from unittest.case import TestCase
from driftchamber.core.datastore import DataStore
from driftchamber.modules.geometry import DetectorGeometry


class DetectorGeometryTest(TestCase):

    def test(self):
        datastore = DataStore()
        geometry = DetectorGeometry(superlayers=4,
                                    layers=[4, 2, 5, 1],
                                    cells=5)
        geometry.begin(datastore)

        detector = datastore.get('detector')

        self.assertEqual(detector.width, 5)
        self.assertEqual(detector.height, 12)
        self.assertEqual(len(detector.superlayers), 4)
        self.assertEqual(detector.superlayers[0].layer_count, 4)
        self.assertEqual(detector.superlayers[1].layer_count, 2)
        self.assertEqual(detector.superlayers[2].layer_count, 5)
        self.assertEqual(detector.superlayers[3].layer_count, 1)
