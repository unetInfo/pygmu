import numpy as np
from extent import Extent
from pyg_pe import PygPE
import soundfile as sf

class WavWriterPE(PygPE):

    def __init__(self, src_pe:PygPE, filename="wav"):
        """
        Write frames to a file as they go whizzing by...
        """
        self._src_pe = src_pe
        self._filename = filename
        self._soundfile = None

    def open(self):
        """
        Open the soundfile from the filename.
        """
        if self._soundfile is None:
            print("opening", self._filename, "for writing")
            self._soundfile = sf.SoundFile(self._filename,
                                           mode='w',
                                           samplerate=self.frame_rate(),
                                           channels=self.channel_count(),
                                           format='WAV',
                                           subtype='FLOAT')
        return self._soundfile

    def close(self):
        """
        Close the soundfile if it is open.
        """
        if self._soundfile is not None:
            print("closing", self._filename)
            self._soundfile.close()
            self._soundfile = None

    def render(self, requested:Extent):
        src_frames = self._src_pe.render(requested)
        overlap = requested.intersect(self.extent())
        # Super special hack with possibly surprising consequences:
        if not overlap.is_empty():
            # some non-empty data arrived.  Open and start writing...
            self.open().write(src_frames.T)
        elif self._soundfile is not None:
            # sample data has been written to the file, but now overlap is
            # zero: stop writing
            self.close()
        # File is not yet open, but no real data yet.  Just pass to output
        return src_frames

    def extent(self):
        return self._src_pe.extent()

    def frame_rate(self):
        return self._src_pe.frame_rate()

    def channel_count(self):
        return self._src_pe.channel_count()
