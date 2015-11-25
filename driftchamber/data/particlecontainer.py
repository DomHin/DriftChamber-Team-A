__author__ = 'Patrick Schreiber'

from itertools import chain


class ParticleContainer:
    def __init__(self):
        self._particles = {}

    def add_particle(self, particle, particle_name):
        if particle_name in self._particles:
            self._particles[particle_name].append(particle)
        else:
            self._particles[particle_name] = [particle]

    def get_particles(self, particle_name):
        return self._particles[particle_name]

    def get_all_particles(self):
        return chain(*self._particles.values())
