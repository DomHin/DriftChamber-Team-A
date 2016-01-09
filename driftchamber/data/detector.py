from numpy import array
from driftchamber.math import point_in_rect


def cell_geometry(cell):
    pos = cell.geometry

    return array([
        [pos[0], pos[1]],
        [pos[0] + cell.width, pos[1]],
        [pos[0], pos[1] + cell.height],
        [pos[0] + cell.width, pos[1] + cell.height]])


def find_cell_in_position(detector, position):
    for cell in detector.cells:
        geometry = cell_geometry(cell)
        if point_in_rect(position, geometry):
            return cell

    return None


class Detector(object):

    def __init__(self, superlayers):
        self._superlayers = superlayers

    @property
    def width(self):
        return self.superlayers[0].width

    @property
    def height(self):
        counts = [superlayer.layer_count for superlayer in self.superlayers]
        return sum(counts)

    @property
    def superlayers(self):
        return self._superlayers

    @property
    def cells(self):
        cells = []

        for superlayer in self.superlayers:
            for layer in superlayer.layers:
                cells.extend(layer.cells)

        return cells


class SuperLayer(object):

    def __init__(self, layers):
        self._layers = layers

    @property
    def layers(self):
        return self._layers

    @property
    def layer_count(self):
        return len(self.layers)

    @property
    def width(self):
        return self.layers[0].width


class Layer(object):

    def __init__(self, cells):
        self._cells = cells

    @property
    def cells(self):
        return self._cells

    @property
    def width(self):
        return len(self._cells)


class Cell(object):

    def __init__(self, position, width=1):
        self._position = position
        self._width = 1
        self._height = 1

    @property
    def position(self):
        return self._position

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __eq__(self, cell):
        pos = self.position
        cell_pos = cell.position

        return pos[0] == cell_pos[0] and pos[1] == cell_pos[1]


class Hit(object):

    def __init__(self, cell, deposited_energy):
        self._cell = cell
        self._deposited_energy = deposited_energy

    @property
    def cell(self):
        return self._cell

    @property
    def deposited_energy(self):
        return self._deposited_energy
