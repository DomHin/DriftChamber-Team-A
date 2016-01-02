from unittest.case import TestCase
from driftchamber.core.datastore import DataStore
from driftchamber.modules.particle_propagator import ParticlePropagator
from driftchamber.modules.geometry import DetectorGeometry

class ParticlePropagatorTest(TestCase):
    
    def setUp(self):
        datastore = DataStore()
        geometry = DetectorGeometry(superlayers=2, 
                                    layers=[3, 5],
                                    layer_cells=10)
        geometry.begin(datastore)
        
        self.propagator = ParticlePropagator()
        #self.propagator.begin(datastore)
        
    def test_propagation(self):
        pass
