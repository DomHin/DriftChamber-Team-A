from driftchamber.core.module import Module

class DetectorGeometry(Module):
    
    def __init__(self, **kwargs):
        self._superlayers = kwargs['superlayers']
        self._layers = kwargs['layers']
        self._cells = kwargs['cells']
