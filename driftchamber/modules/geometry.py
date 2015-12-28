from driftchamber.core.module import Module

class DetectorGeometry(Module):
    
    def __init__(self, **kwargs):
        self._superlayers = kwargs.get('superlayers')
        self._layers = kwargs.get('layers')
        self._cells = kwargs.get('cells')
