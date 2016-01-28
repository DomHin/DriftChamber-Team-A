from numpy import ndarray


class Point2D(ndarray):
    def __new__(cls, x, y):
        arr = ndarray.__new__(Point2D, shape=(2,), dtype=float)
        arr[0] = x
        arr[1] = y
        return arr

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value


class Dimension2D:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class Rectangle2D:
    def __init__(self, pos, dim):
        self._bottom_left = Point2D(pos.x, pos.y)
        self._bottom_right = Point2D(pos.x + dim.width, pos.y)
        self._upper_left = Point2D(pos.x, pos.y + dim.height)
        self._upper_right = Point2D(pos.x + dim.width, pos.y + dim.height)

    @property
    def upper_left(self):
        return self._upper_left

    @property
    def upper_right(self):
        return self._upper_right

    @property
    def bottom_left(self):
        return self._bottom_left

    @property
    def bottom_right(self):
        return self._bottom_right


def point_in_rect(point, rect):
    return rect.upper_left.x <= point.x <= rect.upper_right.x and \
           rect.bottom_left.y <= point.y <= rect.upper_right.y


def sign(x):
    return x / abs(x) if x != 0 else 0
