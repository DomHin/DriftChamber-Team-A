from numpy import array

class Particle(object):

    def __init__(self, name, mass,
                 position = array([0, 0]), 
                 momentum = array([0, 0])):
        self._name = name
        self._mass = mass
        self._position = position
        self._momentum = momentum
    
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
