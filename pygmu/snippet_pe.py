from crop_pe import CropPE
from time_shift_pe import TimeShiftPE
from extent import Extent
from pyg_pe import PygPE
from wav_reader_pe import WavReaderPE
import numpy as np

class SnippetPE(PygPE):
    """
    Play a snippet from a sound file.
    """

    def __init__(self, filename, sync_point=0, crop=None):
        """
        Create a SnippedPE
        @param filename The name of a .wav file containing the sound data.
        @param sync_point The frame within the sound file that is considered
        to be the (perceptual) start, even though some data may precede it.
        @param crop If given, limits playback to a subset of the sound data.

        Note that SnippetPE comprises upto three other PE's: a WavReader to
        read the data from a .wav file, a CropPE to limit what's played, and
        a TimeShiftPE to offset according to the sync_point.
        """
        super(SnippetPE, self).__init__()
        self._src_pe = WavReaderPE(filename)
        self._extent = self._src_pe.extent()
        if crop is not None:
            self._src_pe = CropPE(self._src_pe, crop)
            self._extent = self._extent.intersect(crop)
        if sync_point != 0:
            self._src_pe = TimeShiftPE(self._src_pe, -sync_point)

    def render(self, requested:Extent):
        return self._src_pe.render(requested)

    def extent(self):
        return self._extent

    def frame_rate(self):
        return self._src_pe.frame_rate()

    def channel_count(self):
        return self._src_pe.channel_count()
