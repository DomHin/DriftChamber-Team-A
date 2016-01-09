from unittest.case import TestCase
from nose_parameterized import parameterized
from numpy import array
from driftchamber.math import point_in_rect, sign


class MathTest(TestCase):

    @parameterized.expand([
        (array([4, 6]), array([[2, 3], [10, 3], [2, 13], [10, 13]])),
        (array([10, 13]), array([[2, 3], [10, 3], [2, 13], [10, 13]])),
        (array([4, 6]), array([[4, 6], [12, 6], [4, 16], [12, 16]]))
    ])
    def test_point_in_rect_true(self, point, rect):
        self.assertTrue(point_in_rect(point, rect))

    @parameterized.expand([
        (array([4, 13.01]), array([[2, 3], [10, 3], [2, 13], [10, 13]])),
        (array([3, 6]), array([[4, 6], [12, 6], [4, 16], [12, 16]])),
        (array([3, 17]), array([[4, 6], [12, 6], [4, 16], [12, 16]]))
    ])
    def test_point_in_rect_false(self, point, rect):
        self.assertFalse(point_in_rect(point, rect))

    @parameterized.expand([
        (-7, -1),
        (0, 0),
        (32, 1)
    ])
    def test_sign(self, value, expected_value):
        self.assertEqual(sign(value), expected_value)
