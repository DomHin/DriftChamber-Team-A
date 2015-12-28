from unittest.case import TestCase
from driftchamber.core.datastore import DataStore
from driftchamber.modules.particle_gun import ParticleGun


class ParticleGunTest(TestCase):

    def test(self):
        datastore = DataStore()
        gun = ParticleGun(name='kaon',
                          mass=0.000493667,
                          max_momentum=0.1,
                          max_position_x=100,
                          max_position_y=100)
        gun.event(datastore)

        particle = datastore.get('particle')

        self.assertEqual(particle.name, 'kaon')
        self.assertEqual(particle.mass, 0.000493667)

        self.assertLessEqual(particle.position[0], 100)
        self.assertGreaterEqual(particle.position[0], 0)
        self.assertLessEqual(particle.position[1], 100)
        self.assertGreaterEqual(particle.position[1], 0)
