import random
import logging
from driftchamber.core.particles import Particle
from driftchamber.core.module import Module


class Noise(Module):

    def begin(self, datastore):
        configuration = datastore.get(self)
        self._noiseName = configuration['Particle_name']
        self._noiseMass = configuration['Particle_mass']
        self._noiseProbability = configuration['Particle_prob'] #Probability to have noise per cell
        self._noisePart = Particle(self._noiseMass, self._noiseName) #Creates a "particle", which is flagged as noise
        self._detector = datastore.get('Detector')
        logging.info("Begin of module Noise")

    def event(self, datastore):

        for y in range(self._detector.height): #Loop over layers
            for x in range(self._detector.width): #Loop over cells in one layer
                if random.random() < self._noiseProbability:
                    hit = self._detector.deposit_energy_at((x,y), self._noisePart) #Flag current cell as triggered due to noise
                    n = datastore.get('CurrentEvent')
                    datastore.get('HitObjects').add_hit(hit, n, 'Noise')

    def end(self, datastore):
        logging.info("End of module Noise")




