from unittest.case import TestCase

from numpy.linalg.linalg import norm

from driftchamber.data.particle import Particle
from driftchamber.math import Point2D


class ParticleTest(TestCase):

    def test_energy_momentum_values(self):
        particle = Particle(name='test', mass=0.003)
        particle.momentum = Point2D(0.345, 0.154)

        self.assertAlmostEqual(norm(particle.momentum), 0.37781, 3)
        self.assertAlmostEqual(particle.energy, 0.37782, 3)
