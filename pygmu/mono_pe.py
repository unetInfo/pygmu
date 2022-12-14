import numpy as np
from extent import Extent
from pyg_pe import PygPE

class MonoPE(PygPE):
    """
    Convert a stereo source to mono.  (Or pass a mono source through directly)
    """

    def __init__(self, src_pe, attenuation=1.0):
        super(MonoPE, self).__init__()
        self._src_pe = src_pe
        self._attenuation = attenuation

    def render(self, requested:Extent):
        buf = self._src_pe.render(requested)
        if buf.shape[1] == 2:
            buf = np.dot(buf, [[self._attenuation], [self._attenuation]])
        return buf

    def extent(self):
        return self._src_pe.extent()

    def frame_rate(self):
        return self._src_pe.frame_rate()

    def channel_count(self):
        return 1

