__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module


class ParticlePrinter(Module):

    def __init__(self, config):
        super(ParticlePrinter, self).__init__(config)

    def begin(self, datastore):
        # print("Begin of Simulation of ParticleGun")
        logging.info('Begin of Simulation of ParticlePrinter')

    def event(self, datastore):
        for particle in datastore.get('Particles').get_all_particles():
        # particle = datastore.get(self.particle_name)
            logging.info('Particle: {}'.format(particle.name))

            logging.info(particle.position())
            logging.info(particle.momentum())

    def end(self, datastore):
        # print("End of Simulation of ParticleGun")
        logging.info('End of Simulation of ParticlePrinter')


