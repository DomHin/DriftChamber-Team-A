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

    def __init__(self, width=1):
        self._width = 1

    @property
    def width(self):
        return self._width
