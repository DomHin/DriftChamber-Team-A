__author__ = 'Patrick Schreiber'

import logging

from driftchamber.core.module import Module


class ParticlePrinter(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'ParticlePrinter'")

    def event(self, datastore):
        for particle in datastore.get('Particles').get_all_particles():
        # particle = datastore.get(self.particle_name)
            logging.info('Particle: {}'.format(particle.particle_name))

            logging.info(particle.position())
            logging.info(particle.momentum())

    def end(self, datastore):
        logging.info("End of module 'ParticlePrinter'")


