__author__ = 'Patrick Schreiber'

import unittest
from driftchamber.core.particles import Position, Momentum, Particle

class PositionTest(unittest.TestCase):

    def test_creation_position(self):
        pos = Position(1, 2)
        self.assertEqual(pos.pos(), (1, 2))

    def test_creation_momentum(self):
        mom = Momentum(1, 2)
        self.assertEqual(mom.mom(), (1, 2))

    def test_add_position(self):
        pos1 = Position(1, 2)
        pos2 = Position(2, 3)

        self.assertEqual((pos1+pos2).pos(), (3, 5))

    def test_sub_position(self):
        pos1 = Position(1, 2)
        pos2 = Position(2, 3)

        self.assertEqual((pos1-pos2).pos(), (-1, -1))

    def test_add_momentum(self):
        mom1 = Momentum(1, 2)
        mom2 = Momentum(2, 3)

        self.assertEqual((mom1+mom2).mom(), (3, 5))

    def test_sub_momentum(self):
        mom1 = Momentum(1, 2)
        mom2 = Momentum(2, 3)

        self.assertEqual((mom1-mom2).mom(), (-1, -1))

    def test_fail_add(self):
        pos = Position(1, 2)
        mom = Momentum(1, 2)

        with self.assertRaises(TypeError):
            pos+mom

    def test_particle_position(self):
        P = Particle()
        self.assertEqual(P.position().pos(), (0, 0))
        P = Particle(1, 2)
        self.assertEqual(P.position().pos(), (1, 2))
        P.set_position(4, 5)
        self.assertEqual(P.position().pos(), (4, 5))

    def test_particle_momentum(self):
        P = Particle()
        self.assertEqual(P.momentum().mom(), (0, 0))
        P = Particle(px=1, py=2)
        self.assertEqual(P.momentum().mom(), (1, 2))
        P.set_momentum(4, 5)
        self.assertEqual(P.momentum().mom(), (4, 5))

