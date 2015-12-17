from unittest.case import TestCase
from nose_parameterized import parameterized
from driftchamber.math import Vector, norm

class VectorTest(TestCase):
    
    @parameterized.expand([
        (Vector(2, 4), Vector(3, 5), Vector(5, 9)),
        (Vector(-7, -9), Vector(-4, 30), Vector(-11, 21))
    ])
    def test_vector_sum(self, v1, v2, sum_v):
        self.assertEqual(v1 + v2, sum_v)
        
    @parameterized.expand([
        (Vector(2, 4), Vector(3, 5), Vector(-1, -1)),
        (Vector(-7, -9), Vector(-4, 30), Vector(-3, -39))
    ])
    def test_vector_diff(self, v1, v2, diff_v):
        self.assertEqual(v1 - v2, diff_v)
        
    @parameterized.expand([
        (Vector(2, 4), Vector(3, 5), 26),
        (Vector(-7, -9), Vector(-4, 30), -242)
    ])
    def test_vector_prod(self, v1, v2, prod):
        self.assertEqual(v1 * v2, prod)
        
    @parameterized.expand([
        (Vector(2, 4), 2, Vector(4, 16), 16.49),
        (Vector(2, 4), 5, Vector(32, 1024), 1024.5)
    ])
    def test_vector_pow(self, v, exponent, result_v, norm_val):
        self.assertEqual(v**exponent, result_v)
        self.assertAlmostEqual(norm(v**exponent), norm_val, 2)