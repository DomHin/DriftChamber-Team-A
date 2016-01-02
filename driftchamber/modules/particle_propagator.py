from numpy import array
from driftchamber.core.module import Module
from driftchamber.data.detector import cell_geometry
from driftchamber.math import point_in_rect, sign


class ParticlePropagator(Module):

    def begin(self, datastore):
        self._particle = datastore.get('particle')
        self._detector = datastore.get('detector')

    def event(self, datastore):
        self._propagate()
        self._simulate_cell_hit()

    def _propagate(self):
        pos = self._adjacent_cell_in_flight_path()
        self._particle.position = pos
        
        return pos

    def _adjacent_cell_in_flight_path(self):
        mom = self._particle.momentum
        pos = self._particle.position
        mass = self._particle.mass

        t = self._min_adjacent_cell_flight_duration()
        new_x = pos[0] + mom[0] * t / mass
        new_y = pos[1] + mom[1] * t / mass

        return array([new_x, new_y])

    def _min_adjacent_cell_flight_duration(self):
        dist = self._adjacent_cell_distance()
        mom = self._particle.momentum
        mass = self._particle.mass

        t_x = dist[0] / (mom[0] / mass)
        t_y = dist[1] / (mom[1] / mass)

        return min(t_x, t_y)

    def _adjacent_cell_distance(self):
        cell = self._current_cell()
        pos = cell.position
        mom = self._particle.momentum

        next_x = pos[0] + cell.width * sign(mom[0]) * 1
        next_y = pos[1] + cell.height * sign(mom[1]) * 1

        dist_x = abs(next_x - pos[0])
        dist_y = abs(next_y - pos[1])

        return array([dist_x, dist_y])

    def _current_cell(self):
        particle_pos = self._particle.position

        for cell in self._detector.cells:
            geometry = cell_geometry(cell)

            if point_in_rect(particle_pos, geometry):
                return cell

        return None
    
    def _simulate_cell_hit(self):
        pass
