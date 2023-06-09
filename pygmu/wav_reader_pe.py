import numpy as np
from extent import Extent
from pyg_pe import PygPE
import soundfile as sf

class WavReaderPE(PygPE):
    """
    Read a .wav file.
    """

    def __init__(self, filename):
        super(WavReaderPE, self).__init__()
        self._filename = filename
        self._soundfile = None  # lazy instantiation
        self._extent = None

    def soundfile(self):
        """
        Open the soundfile from the filename.
        """
        if self._soundfile is None:
            self._soundfile = sf.SoundFile(self._filename)

        return self._soundfile

    def close(self):
        """
        Close the soundfile if it is open.
        """
        if self._soundfile is not None:
            self._soundfile.close()
            self._soundfile = None

    def filename(self):
        return self._filename

    def frame_count(self):
        return self.soundfile().frames

    def render(self, requested:Extent):
        """
        Return sample data from the soundfile.

        NOTE: this implementation ignores frame rate: it assumes that the
        frame rate of the Transport equals the frame rate of the soune file.

        NOTE: this implmentation assumes that n_channels equals the channel
        count of the sound file.  It will unceremoniously fail if they differ.
        """
        intersection = requested.intersect(self.extent())
        if intersection.is_empty():
            # no intersection
            dst_buf = np.zeros([self.channel_count(), requested.duration()], np.float32)
        else:
            # the sound file overlaps with some or all of the request

            # optimization: avoid seeking every time.
            if self.soundfile().tell() != intersection.start():
                self.soundfile().seek(int(intersection.start()))

            # read the frames from the source file.
            src_n_frames = int(intersection.duration())
            # Use the .T (transpose) operator to convert from soundfile "channel per column"
            # form to pygmu "channel per row" form.
            src_buf = self.soundfile().read(frames=src_n_frames, dtype=np.float32, always_2d=True).T

            if intersection.equals(requested):
                # full overlap: we can return frames directly from the soundfile
                dst_buf = src_buf
            else:
                # partial overlap.  Allocate a buffer of zeros and replace some
                # of them with sample data from the file.
                dst_buf = np.zeros([self.channel_count(), requested.duration()], np.float32)
                offset = intersection.start() - requested.start()
                dst_buf[:, offset:offset + src_n_frames] = src_buf

        return dst_buf


    def extent(self):
        if self._extent is None:
            self._extent = Extent(0, self.frame_count())
        return self._extent

    def frame_rate(self):
        return self.soundfile().samplerate

    def channel_count(self):
        return self.soundfile().channels

