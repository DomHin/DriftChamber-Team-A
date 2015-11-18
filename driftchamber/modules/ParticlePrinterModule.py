__author__ = 'Patrick Schreiber'

from driftchamber.core.module import Module
import logging

class ParticlePrinter(Module):
    def __init__(self):
        self.particle_name = 'SuperParticle'

    def begin(self, datastore):
        # print("Begin of Simulation of ParticleGun")
        logging.info('Begin of Simulation of ParticleGun')

    def event(self, datastore):
        particle = datastore.get(self.particle_name)
        logging.info('Particle: {}'.format(self.particle_name))

        logging.info(particle.position())
        logging.info(particle.momentum())

    def end(self, datastore):
        # print("End of Simulation of ParticleGun")
        logging.info('End of Simulation of ParticleGun')


