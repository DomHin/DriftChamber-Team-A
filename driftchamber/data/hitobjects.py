__author__ = 'Patrick Schreiber'

class HitObjects:
    def __init__(self):
        self._objects = {}

    def add_hit(self, hit, event_number, particle_name):
        if particle_name in self._objects:
            if event_number in self._objects[particle_name]:
                self._objects[particle_name][event_number].append(hit)
            else:
                self._objects[particle_name][event_number] = [hit]
        else:
            self._objects[particle_name] = {event_number: [hit]}

    def get_hits(self, event_number, particle_name):
        return self._objects[particle_name][event_number]
