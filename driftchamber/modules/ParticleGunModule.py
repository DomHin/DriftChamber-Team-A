__author__ = 'Patrick Schreiber'

import random

from driftchamber.core.module import Module
from driftchamber.core.particles import Particle

class ParticleGun(Module):

    def __init__(self):
        self.particle_name = 'SuperParticle' # maybe make this settable in config

    def begin(self, datastore):
        self.particle_name = 'SuperParticle' # maybe make this settable in config
        x = random.random()
        x_mom = random.random()
        y_mom = random.random()

        particle = Particle(x, 0, x_mom, y_mom)
        datastore.put(self.particle_name, particle)

