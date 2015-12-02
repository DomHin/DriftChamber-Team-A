import random


class Cell:
    def __init__(self, position):
        self.deposited_energy = 0
        self.triggered = False
        self.pos = position  # in (x, y) - Tupel

    def deposit_energy(self, particle):
        energy = particle.particle_mass * random.random()
        self.triggered = energy > 0
        # calculate energy to deposit if any
        self.deposited_energy += energy
        particle.subtract_energy(energy)

    def is_triggered(self):
        return self.triggered

    def print_info(self):
        """
        Returns all information necessary for printing
        """
        return self.pos, self.triggered

    def energy(self):
        return self.deposited_energy

    def reset(self):
        self.deposited_energy = 0
        self.triggered = False


class Layer:
    def __init__(self, width, position_y=0):
        self.pos = position_y  # lower left corner of detector array
        self.width = width  # amount of cells per line
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
    def __init__(self, width, nSuperLayers, nLayersList):
        """
        Create detector
        with 'nSuperLayers' amount of super layers
        and for each super layer the amount of layers
        :param int width: Width of the drift chamber
        :param int nSuperLayers: Number of super layers
        :param list of int nLayersList: A list, which entries hold the number of layers for the super layer that 
                                        corresponds to the index of the entry
        """
        self.width = width
        self.nSuperLayers = nSuperLayers
        self.nLayersList = nLayersList
        self.detector = []
        cPos = 0
        for i in range(self.nSuperLayers):
            self.detector.append(SuperLayer(self.width, self.nLayersList[i], position=cPos))
            cPos += self.nLayersList[i]
        self.height = cPos
        self._generate_position_to_superlayer_map()

    def _generate_position_to_superlayer_map(self):
        self.map = {}
        idx = 0
        for slidx, layers in enumerate(self.nLayersList):
            for _ in range(layers):
                self.map[idx] = slidx
                idx += 1

    def deposit_energy_at(self, pos, particle):  # position as (x,y)
        """
        deposits energy at the cell at position (x,y) for particle particle
        """
        sl = self.detector[self.map[int(round(pos[1]))]]
        layer_pos = pos[1] - sl.pos
        layer = sl.layers[int(round(layer_pos))]
        layer.cells[int(round(pos[0]))].deposit_energy(particle)
        return

    def reset(self):
        for idx, sl in enumerate(self.detector):
            for layer in sl.layers:
                for cell in layer.cells:
                    cell.reset()
        

