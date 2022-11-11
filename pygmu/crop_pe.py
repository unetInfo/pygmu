import numpy as np
from extent import Extent
from pyg_pe import PygPE

class CropPE(PygPE):
    """
    Crop the start and/or end time of a PE
    """

    def __init__(self, pe, extent):
        self._pe = pe
        self._extent = extent.intersect(pe.extent())

    def render(self, requested, n_channels):
        return self._pe.render(requested, n_channels)

    def extent(self):
        return self._extent
