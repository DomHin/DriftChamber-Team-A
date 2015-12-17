from unittest.case import TestCase
from nose_parameterized import parameterized
from driftchamber.math import Vector

class VectorTest(TestCase):
    
    @parameterized.expand([
        (Vector(2, 4), Vector(3, 5), Vector(5, 9), Vector(-1, -1), 26),
        (Vector(-7, -9), Vector(-4, 30), Vector(-11, 21), Vector(-3, -39), -242)
    ])
    def test_vector_operations(self, v1, v2, sum_v, diff_v, prod):
        self.assertIsNotNone(v1.x)
        self.assertIsNotNone(v1.y)
        self.assertIsNotNone(v2.x)
        self.assertIsNotNone(v2.y)
        
        self.assertEqual(v1 + v2, sum_v)
        self.assertEqual(v1 - v2, diff_v)
        self.assertEqual(v1 * v2, prod)
        self.assertNotEqual(sum_v, diff_v)