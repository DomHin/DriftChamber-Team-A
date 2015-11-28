import random
import logging
from driftchamber.core.particles import Particle
from driftchamber.core.module import Module


class Noise(Module):

    def begin(self, datastore):
        self._noiseProbability =0.0005 #Probability of noise per event and cell
        self._noiseMass =0.001 #Mass of the Noise-"Particle" determines the average energy deposit
        self._noisePart = Particle(self._noiseMass, 'Noise') #Creates a "particle", which is flagged as noise
        self._detector = datastore.get('Detector')
        logging.info("Begin of module Noise")

    def event(self, datastore):

        for y in range(self._detector.height): #Loop over layers
            for x in range(self._detector.width): #Loop over cells in one layer
                if random.random() < self._noiseProbability:
                    hit = self._detector.deposit_energy_at((x,y), self._noisePart)
                    n = datastore.get('CurrentEvent')
                    datastore.get('HitObjects').add_hit(hit, n, 'Noise')

    def end(self, datastore):
        logging.info("End of module Noise")




