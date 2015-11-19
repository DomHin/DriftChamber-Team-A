__author__ = 'Patrick Schreiber'

import random
import logging

from driftchamber.core.module import Module
from driftchamber.core.particles import Particle

class ParticleGun(Module):
    cells = 50 #Number of cells in a drift chamber layer
    max_mom = 100 #[GEV]temporary definition of maximum momentum, should maybe done in config file

    def __init__(self):
        self.particle_name = 'SuperParticle' # maybe make this settable in config



    def begin(self, datastore):
        # print("Begin of Simulation of ParticleGun")
        logging.info('Begin of Simulation of ParticleGun')

    def event(self, datastore):
        #self.number_of_events += 1
        # print("Number of previous Events: " + str(self.number_of_events))
        x = int(random.random()*self.cells) #transformation to integer cell
        x_mom = (random.random()-0.5)*2*self.max_mom #negative x-direction possible
        y_mom = random.random()*self.max_mom #negative y-direction not possible

        particle = Particle(x, 0, x_mom, y_mom)
        datastore.put(self.particle_name, particle)

    def end(self, datastore):
        # print("End of Simulation of ParticleGun")
        logging.info('End of Simulation of ParticleGun')






