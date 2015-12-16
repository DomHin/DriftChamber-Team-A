class Vector(object):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)
    
    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y
    
    def __ne__(self, vec):
        return not self == vec