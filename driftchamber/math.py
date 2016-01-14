from numpy import array


class Point2D(array):

    def __init__(self, x, y):
        super().__init__(x, y)

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


class Dimension2D(array):

    def __init(self, width, height):
        super().__init__(width, height)

    @property
    def width(self):
        return self[0]

    @property
    def height(self):
        return self[1]


class Rectangle2D(array):
    
    def __init__(self, pos, dim):
        super().__init__([
            [pos.x, pos.y],
            [pos.x + dim.width, pos.y],
            [pos.x, pos.y + dim.height],
            [pos.x + dim.width, pos.y + dim.height]
        ])

def point_in_rect(point, rect):
    return point[0] >= rect[0][0] and \
            point[0] <= rect[1][0] and \
            point[1] >= rect[0][1] and \
            point[1] <= rect[2][1]


def sign(x):
    return x / abs(x) if x != 0 else 0
