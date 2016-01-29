__author__ = 'Patrick Schreiber'

import logging
import random

from driftchamber.core.datastore import NotFoundInDataStore
from driftchamber.core.module import Module
from driftchamber.core.particles import Particle
from driftchamber.data.particlecontainer import ParticleContainer


class ParticleGun(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'ParticleGun'")
        configuration = datastore.get(self)
        self.particle_name = configuration['Particle_name']
        self.particle_mass = configuration['Particle_mass']
        self.particle_max_mom = configuration['Particle_max_mom']
        self.particle_x_pos = configuration['Particle_x_pos']
        self.particle_y_pos = configuration['Particle_y_pos']
        self.particle_x_mom = configuration['Particle_x_mom']
        self.particle_y_mom = configuration['Particle_y_mom']
        self.cells = 100  # Default value when no detector is found (for example in test case)
        self.layers = 36
        try:
            self.cells = datastore.get('Detector').width
            self.layers = datastore.get('Detector').height
        except NotFoundInDataStore:
            logging.warning("ParticleGun hasn't found detector, set cells to default.")
        logging.info("Particle gun initialized that shoots a '" + self.particle_name + "'.")

    def event(self, datastore):
        try:
            datastore.get('Particles')
        except NotFoundInDataStore:
            datastore.put('Particles', ParticleContainer())

        if self.particle_x_pos == -1:
            x_pos = int(random.random()*self.cells)  # transformation to integer cell
        else:
            x_pos = self.particle_x_pos
        if self.particle_y_pos == -1:
            y_pos = int(random.random()*self.layers)  # transformation to integer cell
        else:
            y_pos = self.particle_y_pos
        if self.particle_x_mom == -1:
            x_mom = (random.random()-0.5)*2*self.particle_max_mom  # negative x-direction possible
        else:
            x_mom = self.particle_x_mom
        if self.particle_y_mom == -1:
            y_mom = random.random()*self.particle_max_mom  # negative y-direction not possible
        else:
            y_mom = self.particle_y_mom

        particle = Particle(self.particle_mass, self.particle_name, x_pos, y_pos, x_mom, y_mom)
        datastore.get('Particles').add_particle(particle, self.particle_name)

    def end(self, datastore):
        logging.info("End of module 'ParticleGun'")






