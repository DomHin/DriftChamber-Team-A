import random
import logging
from driftchamber.core.particles import Particle
from driftchamber.core.module import Module


class Noise(Module):

    def begin(self, datastore):
        logging.info("Begin of module 'Noise'")
        configuration = datastore.get(self)
        self._noise_name = configuration['Particle_name']
        self._noise_mass = configuration['Particle_mass']
        self._noise_probability = configuration['Particle_probability'] #Probability to have noise per cell
        self._noise_part = Particle(self._noise_mass, self._noise_name) #Creates a "particle", which is flagged as noise
        self._detector = datastore.get('Detector')
        

    def event(self, datastore):

        for y in range(self._detector.height): #Loop over layers
            for x in range(self._detector.width): #Loop over cells in one layer
                if random.random() < self._noise_probability:
                    hit = self._detector.deposit_energy_at((x,y), self._noise_part) #Flag current cell as triggered due to noise
                    n = datastore.get('CurrentEvent')
                    datastore.get('HitObjects').add_hit(hit, n, 'Noise')

    def end(self, datastore):
        logging.info("End of module 'Noise'")




