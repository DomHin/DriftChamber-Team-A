from random import random

from driftchamber.core.module import Module
from driftchamber.data.detector import Hit, find_cell_in_position
from driftchamber.math import sign


class ParticlePropagator(Module):

    def begin(self, datastore):
        self._particle = datastore.get('particle')
        self._detector = datastore.get('detector')

    def event(self, datastore):
        self._propagate_to_adjacent_cell()
        cell = find_cell_in_position(self._detector, self._particle.position)
        if cell is not None:
            hit = self._hit_cell(cell)
            datastore.add('hits', hit)

    def _propagate_to_adjacent_cell(self):
        momentum = self._particle.momentum
        cell = find_cell_in_position(self._detector, self._particle.position)

        next_x = cell.position[0] + cell.width * sign(momentum[0]) * 1
        next_y = cell.position[1] + cell.height * sign(momentum[1]) * 1

        dist_x = abs(next_x - cell.position[0])
        dist_y = abs(next_y - cell.position[1])

        mass = self._particle.mass

        t_x = dist_x / (momentum[0] / mass)
        t_y = dist_y / (momentum[1] / mass)
        t = min(t_x, t_y)

        self._particle.position[0] += momentum[0] * t / mass
        self._particle.position[1] + momentum[1] * t / mass

    def _hit_cell(self, cell):
        mass = self._particle.mass
        deposited_energy = mass * random()
        self._particle.energy -= deposited_energy

        return Hit(cell, deposited_energy)
