__author__ = 'Patrick Schreiber'

import random
import logging

from driftchamber.core.module import Module
from driftchamber.core.particles import Particle
from driftchamber.core.datastore import NotFoundInDataStore, ObjectLifetime
from driftchamber.data.particlecontainer import ParticleContainer

class ParticleGun(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'ParticleGun'")
        configuration = datastore.get(self)
        self.particle_name = configuration['Particle_name']
        self.particle_mass = configuration['Particle_mass']
        self.particle_max_mom = configuration['Particle_max_mom']
        self.cells = datastore.get('Detector').width
        try:
            datastore.get('Particles')
        except NotFoundInDataStore:
            datastore.put('Particles', ParticleContainer(), ObjectLifetime.Application)
        logging.info("Particle gun initialized that shoots a '" + self.particle_name + "'.")

    def event(self, datastore):
        x = int(random.random()*self.cells)  # transformation to integer cell
        x_mom = (random.random()-0.5)*2*self.particle_max_mom  # negative x-direction possible
        y_mom = random.random()*self.particle_max_mom  # negative y-direction not possible
        particle = Particle(self.particle_mass, self.particle_name, x, 0, x_mom, y_mom)
        datastore.get('Particles').add_particle(particle, self.particle_name)

    def end(self, datastore):
        logging.info("End of module 'ParticleGun'")






