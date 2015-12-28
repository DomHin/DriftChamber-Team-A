from unittest.case import TestCase
from driftchamber.core.datastore import DataStore
from driftchamber.modules.particle_gun import ParticleGun

class ParticleGunTest(TestCase):
    
    def setUp(self):
        self._datastore = DataStore()
        self._gun = ParticleGun(name='kaon',
                                mass=0.000493667, 
                                max_momentum=0.1,
                                max_position_x=100,
                                max_position_y=100)
    
    def test(self):
        self._gun.event(self._datastore)
        
        particle = self._datastore.get('particle')
        
        self.assertEqual(particle.name, 'kaon')
        self.assertEqual(particle.mass, 0.000493667)
        
        self.assertLessEqual(particle.position[0], 100)
        self.assertGreaterEqual(particle.position[0], 0)
        self.assertLessEqual(particle.position[1], 100)
        self.assertGreaterEqual(particle.position[1], 0)
