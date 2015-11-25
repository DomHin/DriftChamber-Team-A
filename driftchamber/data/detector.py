import matplotlib.pyplot as plt

import random
from driftchamber.data.hit import HitObject


class Cell:
    def __init__(self, position):
        self.deposited_energy = 0
        self.triggered = False
        self.pos = position  # in (x, y) - Tupel

    def deposit_energy(self, particle):
        energy = particle.mass * random.random()
        self.triggered = energy > 0
        # calculate energy to deposit if any
        self.deposited_energy += energy
        particle.subtract_energy(energy)

    def been_hit(self):
        return self.triggered

    def print_info(self):
        """
        Returns all information necessary for printing
        """
        return self.pos, self.triggered

    def energy(self):
        return self.deposited_energy


class Layer:
    def __init__(self, width, position_y=0):
        self.pos = position_y  # lower left corner of detectorarray
        self.width = width  # Amount of cells per line
        # self.stack = lines  # Amount of stacked cell_lines

        self.cells = []  # Generate all cells for Layer
        # for s in range(self.stack):
        #     line = []
        for l in range(self.width):
            self.cells.append(Cell(position=(l, self.pos)))  # postition = layer_offset + l-th cell
        # self.cells = [ line1, line2, ... ]
        # lineX = [cell1, cell2, ...]


class SuperLayer:
    def __init__(self, width, layers, position):
        """
        width INT total width of detector
        layers INT
        """
        self.width = width
        self.pos = position

        self.layers = []
        for i in range(layers):
            self.layers.append(Layer(self.width, position_y=i+self.pos))
        # self.layers = [layer1, layer2, ... ]


class Detector:
    def __init__(self, width, superlayers, layer_info):
        """
        Create detector
        with 'superlayers' amount of Superlayers
        and for each Superlayer the amount of layers
        :param int width: Width of the driftchamber
        :param int superlayers: Number of superlayers
        :param list of int layer_info: List with each entry is the number of layers for the superlayer that corres
                                       ponds to the index
        """
        self.width = width
        self.superlayers = superlayers
        self.layer_info = layer_info
        self.detector = []
        cPos = 0
        for i in range(self.superlayers):
            self.detector.append(SuperLayer(self.width, self.layer_info[i], position=cPos))
            cPos += self.layer_info[i]
        self.height = cPos
        self._generate_position_to_superlayer_map()

    def _generate_position_to_superlayer_map(self):
        self.map = {}
        idx = 0
        for slidx, layers in enumerate(self.layer_info):
            for l in range(layers):
                self.map[idx] = slidx
                idx += 1

    def deposit_energy_at(self, pos, particle):  # position as (x,y)
        """
        deposits energy at the cell at position (x,y) for particle particle
        """
        sl = self.detector[self.map[pos[1]]]
        layer_pos = pos[1] - sl.pos
        layer = sl.layers[layer_pos]
        layer.cells[pos[0]].deposit_energy(particle)
        return HitObject(pos, 1, layer.cells[pos[0]])


    def print(self):
        """
        Insert Code to print the detector cells
        Position of this function will probably changPosition of this function will probably change
        """
        symbols = ['o', 'x', 'O', 'X', ':', '.', 'I', '-', '#', '@']
        for index, sl in enumerate(self.detector):
            for layer in sl.layers:
                for cell in layer.cells:
                    print(symbols[index % len(symbols)], end='')
                print('')

    def show(self):
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'black', 'magenta', 'purple', 'lightblue', 'grey']
        for idx, sl in enumerate(self.detector):
            for layer in sl.layers:
                for cell in layer.cells:
                    fillstyle = 'full' if cell.been_hit() else 'none'
                    plt.plot(cell.pos[0], cell.pos[1], marker='s', fillstyle=fillstyle, color=colors[idx % len(colors)])
        plt.ylim(-0.5, self.height-0.5)
        plt.show()

