from unittest.case import TestCase
from nose_parameterized import parameterized
from numpy import array
from driftchamber.physics import relativistic_energy

class PhysicsTest(TestCase):
    
    @parameterized.expand([
        (20, array([44, 57]), 64.67)
    ])
    def test_relativistic_energy(self, mass, momentum, expected_energy):
        energy = relativistic_energy(mass, momentum)
        
        self.assertAlmostEqual(energy, expected_energy, 2)
