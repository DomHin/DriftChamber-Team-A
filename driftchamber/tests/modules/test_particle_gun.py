from unittest.case import TestCase
from driftchamber.core.datastore import DataStore
from driftchamber.modules.particle_gun import ParticleGun


class ParticleGunTest(TestCase):

    def setUp(self):
        datastore = DataStore()
        gun = ParticleGun(name='kaon',
                          mass=0.000493667,
                          max_momentum=0.1,
                          max_position_x=100,
                          max_position_y=100)
        gun.begin(datastore)

        self.particle = datastore.get('particle')

    def test_particle(self):
        self.assertEqual(self.particle.name, 'kaon')
        self.assertEqual(self.particle.mass, 0.000493667)

        self.assertLessEqual(self.particle.position[0], 100)
        self.assertGreaterEqual(self.particle.position[0], 0)
        self.assertLessEqual(self.particle.position[1], 100)
        self.assertGreaterEqual(self.particle.position[1], 0)
