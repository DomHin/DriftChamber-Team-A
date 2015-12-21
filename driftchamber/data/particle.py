from driftchamber.math import Vector, norm

class Particle(object):

    def __init__(self, name, mass, momentum = Vector(0, 0)):
        self._name = name
        self._mass = mass
        self._momentum = momentum
    
    @property
    def name(self):
        return self._name
        
    @property
    def momentum(self):
        return self._momentum

    @momentum.setter
    def momentum(self, value):
        self._momentum = value
    
    @property
    def energy(self):
        return (self.mass**2 + norm(self.momentum**2))**0.5

    @energy.setter
    def energy(self, value):
        pass
