from driftchamber.core.module import Module

class DetectorGeometry(Module):
    
    def __init__(self, superlayers, layers, cells):
        self._superlayers = superlayers
        self._layers, self._cells = layers, cells