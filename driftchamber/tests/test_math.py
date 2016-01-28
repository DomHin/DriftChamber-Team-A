from unittest.case import TestCase
from nose_parameterized import parameterized
from driftchamber.math import Point2D, Rectangle2D, Dimension2D, \
                                point_in_rect, sign


class MathTest(TestCase):

    @parameterized.expand([
        (Point2D(4, 6), Rectangle2D(Point2D(2, 3), Dimension2D(8, 10))),
        (Point2D(10, 13), Rectangle2D(Point2D(2, 3), Dimension2D(8, 10))),
        (Point2D(4, 6), Rectangle2D(Point2D(4, 6), Dimension2D(8, 10)))
    ])
    def test_point_in_rect_true(self, point, rect):
        self.assertTrue(point_in_rect(point, rect))

    @parameterized.expand([
        (Point2D(4, 13.01), Rectangle2D(Point2D(2, 3), Dimension2D(8, 10))),
        (Point2D(3, 16), Rectangle2D(Point2D(2, 3), Dimension2D(8, 10))),
        (Point2D(3, 17), Rectangle2D(Point2D(4, 6), Dimension2D(8, 10)))
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
