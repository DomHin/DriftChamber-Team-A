from numpy import array
from numpy.linalg.linalg import norm
from driftchamber.physics import relativistic_energy, relativistic_momentum


class Particle(object):

    def __init__(self, **kwargs):
        self._name = kwargs.get('name')
        self._mass = kwargs.get('mass')

        self._position = kwargs.get('position', array([0, 0]))
        self._momentum = kwargs.get('momentum', array([0, 0]))

    @property
    def name(self):
        return self._name

    @property
    def mass(self):
        return self._mass

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def momentum(self):
        return self._momentum

    @momentum.setter
    def momentum(self, value):
        self._momentum = value

    @property
    def at_rest(self):
        return norm(self.momentum) == 0

    @property
    def energy(self):
        return relativistic_energy(self.mass, self.momentum)

    @energy.setter
    def energy(self, value):
        new_momentum = relativistic_momentum(value, self.mass)

        if value < self.mass or self.at_rest:
            self.momentum = array([0, 0])
        else:
            ratio = new_momentum / self.momentum
            self.momentum[0] *= ratio
            self.momentum[1] *= ratio
