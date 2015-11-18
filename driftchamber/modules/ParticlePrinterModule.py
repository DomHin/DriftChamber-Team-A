__author__ = 'Patrick Schreiber'

from driftchamber.core.module import Module

class ParticlePrinter(Module):

    def __init__(self):
        self.particle_name = 'SuperParticle'

    def begin(self, datastore):
        print('Particle: {}'.format(self.particle_name))
        particle = datastore.get(self.particle_name)
        print(particle.position())
        print(particle.momentum())
