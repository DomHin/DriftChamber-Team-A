__author__ = 'Patrick Schreiber'

import random
import logging

from driftchamber.core.module import Module
from driftchamber.core.particles import Particle
from driftchamber.core.datastore import NotFoundInDataStore
from driftchamber.data.particlecontainer import ParticleContainer

class ParticleGun(Module):
    max_mom = 0.01  # [GEV]temporary definition of maximum momentum, should maybe done in config file
    index = 100

    def __init__(self, config):
        super(ParticleGun, self).__init__(config)
        self.particle_name = self.config[0] if self.config else 'MissingName'  # maybe make this settable in config
        self.particle_mass = 0.000501  # [GeV] aka electron = 501 MeV

    def begin(self, datastore):
        # print("Begin of Simulation of ParticleGun")
        logging.info('Begin of Simulation of ParticleGun')
        self.cells = datastore.get('Detector').width

    def event(self, datastore):
        try:
            datastore.get('Particles')
        except NotFoundInDataStore:
            datastore.put('Particles', ParticleContainer())

        x = int(random.random()*self.cells)  # transformation to integer cell
        x_mom = (random.random()-0.5)*2*self.max_mom  # negative x-direction possible
        y_mom = random.random()*self.max_mom  # negative y-direction not possible
        particle = Particle(self.particle_mass, self.particle_name, x, 0, x_mom, y_mom)
        datastore.get('Particles').add_particle(particle, self.particle_name)

    def end(self, datastore):
        # print("End of Simulation of ParticleGun")
        logging.info('End of Simulation of ParticleGun')






