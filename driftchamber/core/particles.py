__author__ = 'Patrick Schreiber'

class Vector(object):
    """
    Class container for vectors (Position, Momentum etc.)
    """
    vType = 'Vector'

    def __init__(self, x, y):
        """
        Initialise a vector
        :param x: x-value
        :param y: y-value
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        if issubclass(other.__class__, Vector):
            if other.vType == self.vType:
                return self.__class__(self.x+other.x, self.y+other.y)
            else:
                raise TypeError("Cannot add Vector of type " + self.vType + " and Vector of type "+other.vType)
        else:
            raise TypeError("Cannot add Vector of type " + self.vType + " and "+other.__class__.__name__)

    def __sub__(self, other):
        if issubclass(other.__class__, Vector):
            if other.vType == self.vType:
                return self.__class__(self.x-other.x, self.y-other.y)
            else:
                raise TypeError("Cannot subtract Vector of type " + self.vType + " and Vector of type "+other.vType)
        else:
            raise TypeError("Cannot subtract Vector of type " + self.vType + " and "+other.__class__.__name__)


class Position(Vector):
    """
    Class container for positions
    """
    vType = 'Position'

    def pos(self):
        """
        Get the position as tuple
        :return: (x, y)
        """
        return self.x, self.y

    def __str__(self):
        return 'Position\nx={}\ny={}'.format(self.x, self.y)



class Momentum(Vector):
    """
    Class container for Momentum
    """
    vType = 'Momentum'

    def mom(self):
        """
        Get the momentum as tuple
        :return: (px, py)
        """
        return self.x, self.y

    def __str__(self):
        return 'Momentum\np_x={}\np_y={}'.format(self.x, self.y)


class Particle(object):
    """
    Class representing a particle
    """
    def __init__(self, x=None, y=None, px=None, py=None, pos=None, mom=None):
        """
        Initialise a particle
        Either initialise using x, y, px, py (omitted values will be treated as 0)
        or using pos and mom (omitted values will be treated as 0)
        :param x: x-position
        :param y: y-position
        :param px: x-momentum
        :param py: y-momentum
        :param pos: instance of Position
        :param mom: instance of Momentum
        :return:
        """
        if pos:
            self.pos = pos
        else:
            _x = x if x else 0
            _y = y if y else 0
            self.pos = Position(_x, _y)
        if mom:
            self.mom = mom
        else:
            _x_momentum = px if px else 0
            _y_momentum = py if py else 0
            self.mom = Momentum(_x_momentum, _y_momentum)

    def set_position(self, x=None, y=None, pos=None):
        """
        Set the position of a Particle. if pos is given x and y are ignored if not and x or y are omitted, they are
        treated as 0
        :param x: x-Value
        :param y: y-Value
        :param pos: Position object
        :return:
        """
        if pos:
            self.pos = pos
        else:
            _x = x if x else 0
            _y = y if y else 0
            self.pos = Position(_x, _y)

    def set_momentum(self, px=None, py=None, mom=None):
        """
        Set the Momentum of a Particle. if mom is given px and py are ignored if not and px or py are omitted, they are
        treated as 0
        :param px: x-Momentum
        :param py: y-Momentum
        :param mom: Position object
        :return:
        """
        if mom:
            self.mom = mom
        else:
            _x = px if px else 0
            _y = py if py else 0
            self.mom = Momentum(_x, _y)

    def position(self):
        """
        Get the position
        :return: Position object
        """
        return self.pos

    def momentum(self):
        """
        Get the momentum
        :return: Momentum object
        """
        return self.mom
