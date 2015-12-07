__author__ = 'Patrick Schreiber'



class HitObject(object):
    def __init__(self, pos, energy, cell=None):
        """
        Object that describes a Hit event.
        :param tuple pos: position as touple of (x, y)
        :param energy: the energy of the HitObject
        :param cell: reference to the cell that was hit
        :return:
        """
        self.pos = pos
        self.energy = energy
        self.cell = cell
