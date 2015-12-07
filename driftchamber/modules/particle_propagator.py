__author__ = 'Patrick Schreiber'

from driftchamber.core.module import Module


class ParticlePropagator(Module):

    def begin(self, datastore):
        self._detector = datastore.get('Detector')


    def event(self, datastore):
        """
        Propagate a particle through the detector
        :param datastore: reference to datastore
        """
        for particle in datastore.get('Particles').get_all_particles():
            if particle.position().x < 0 or particle.position().x >= self._detector.width or \
                            particle.position().y < 0 or particle.position().y >= self._detector.height:
                pass
            else:
                self._detector.deposit_energy_at((particle.position().x, particle.position().y), particle)
                while self._propagation_step(particle, datastore):
                    pass

    def _propagation_step(self, particle, datastore):
        """
        Propagate a particle into the next cell
        This calculates totally inrelativistic
        :param particle: the particle to propagate
        :param datastore: reference to the datastore
        """
        cell_pos = lambda x: list(map(int, x))
        sign = lambda x: x/abs(x)
        init_pos = [particle.position().x, particle.position().y]
        momentum = particle.mom
        if momentum.x == 0 and momentum.y == 0:
            return False

        # calculate distance in x and y plane to the next cell
        x_dist = (init_pos[0] - (int(init_pos[0]) + 1 * sign(momentum.x)))
        y_dist = (init_pos[1] - (int(init_pos[1]) + 1 * sign(momentum.y)))
        # calculate the flight duration
        x_dur = abs(x_dist / (momentum.x / particle.particle_mass))
        y_dur = abs(y_dist / (momentum.y / particle.particle_mass))

        # set particle into the nearest cell using the flight duration
        if x_dur < y_dur:
            x = particle.position().x + momentum.x / particle.particle_mass * x_dur
            y = particle.position().y + momentum.y / particle.particle_mass * x_dur
        else:
            x = particle.position().x + momentum.x / particle.particle_mass * y_dur
            y = particle.position().y + momentum.y / particle.particle_mass * y_dur

        particle.set_position(x=x, y=y)

        # return false if particle is outside of detector
        if 0 <= cell_pos([x, y])[0] < self._detector.width and 0 <= cell_pos([x, y])[1] < self._detector.height:
            self._detector.deposit_energy_at(cell_pos([x, y]), particle)
            return True
        else:
            return False

