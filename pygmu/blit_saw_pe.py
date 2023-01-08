import warnings
import numpy as np
from scipy import signal
from extent import Extent
from pyg_pe import PygPE
import pyg_exceptions as px
import utils as ut

"""
From 
https://github.com/thestk/stk/blob/master/include/BlitSaw.h
https://github.com/thestk/stk/blob/master/src/BlitSaw.cpp

BlitSaw( StkFloat frequency = 220.0 ); =>
  nharmonics_ = 0   // choose max # of harmonics without aliasing
  this->reset(); =?
    phase_ = 0;
    state_ = 0;
    lastframe[0] = 0;
  this->setFrequency(220.0); =>
    p_ = frame_rate() / frequency;  // frames per period 48000/220 => 218.18
    C2_ = 1 / p_;                   // periods per frame
    rate_ = PI * C2_;               // d_radians per frame (phase increment)
  this->updateHarmonics(); =>       // setFrequency must have been called (to set p_)
    if (nHarmonics_ <= 0) {
      m_ = 2 * int(floor(0.5 * p_))
    } else {
      m_ = 2 * nHarmonics_ + 1
    }
    a_ = m_ / p_; 


setHarmonics(n) =>    // must be called after setFrequency and before calling tick
  nHarmonics_ = n;
  this->updateHarmonics();
  state_ = -0.5 * a_;


tick():
  // usually:
  // tmp = sin(m_ * phase_) / p_ * sin(phase_) 

  den = sin(phase_);
  if (abs(den) <= EPSILON) {
    tmp = a_;
  } else {
    tmp = sin(m_ * phase_) / p_ * den;
  }

  tmp += state_ - C2_;
  state_ = tmp * 0.995;            // leaky integrator

  phase_ += rate_;                 // advance phase
  if (phase_ >= PI) phase_ -= PI;  // keep phase bounded
  return tmp;
"""

EPSILON = 0.00001   # could be better...

class BlitSawPE(PygPE):
    """
    Band Limited Impulse Train, generating bandlimited pulse or sawtooth waves
    Version B with dynamic frequency input.
    """

    SAWTOOTH = 'sawtooth'

    def __init__(self, frequency=440.0, n_harmonics=0, frame_rate=None):
        """
        Band-limited Impulse Train (BLIT) Sawtooth
        frequency sets the frequency (in conjunction with frame rate)
        n_harmonics is the number of harmonics / 2.  Defaults to frame_rate / freq.
        """
        super(BlitSawPE, self).__init__()
        self._n_harmonics = 0
        if frame_rate is None:
            raise pyx.ArgumentError("frame_rate must be specified")
        self._frame_rate = frame_rate
        self._frequency = frequency
        self.reset()
        if isinstance(self._frequency, PygPE):
            self.set_frequency(440)  # initialize _p, etc...
        else:
            self.set_frequency(frequency)
        self.set_harmonics(n_harmonics)

    def render(self, requested:Extent):
        """
        Band limited pulse train: y(n) = (_m / _period) * sinc(_m * n / _p)
        """
        if isinstance(self._frequency, PygPE):
            return self.render_dynamic(requested)
        else:
            return self.render_fixed(requested)

    def render_fixed(self, requested):
        dst_frames = ut.const_frames(0.0, requested.duration(), 1)
        for idx in range(len(dst_frames)):
            den = np.sin(self._phase)
            if np.abs(den) <= EPSILON:
                tmp = self._a
            else:
                tmp = np.sin(self._m * self._phase) / (self._p * den)

            tmp += self._state - self._C2
            self._state = tmp * 0.995

            self._phase = np.mod(self._phase + self._rate, np.pi)
            
            dst_frames[idx] = tmp

        return dst_frames

    def render_dynamic(self, requested):
        """
        Similar to render_fixed(), but updates frequency on each frame
        """
        freqs = self._frequency.render(requested).reshape(-1)  # convert to 1D array
        dst_frames = ut.uninitialized_frames(requested.duration(), 1)
        for idx in range(len(dst_frames)):
            self.set_frequency(freqs[idx])
            den = np.sin(self._phase)
            if np.abs(den) <= EPSILON:
                tmp = self._a
            else:
                tmp = np.sin(self._m * self._phase) / (self._p * den)

            tmp += self._state - self._C2
            self._state = tmp * 0.995

            self._phase = np.mod(self._phase + self._rate, np.pi)

            dst_frames[idx] = tmp

        return dst_frames

    def channel_count(self):
        return 1

    def frame_rate(self):
        return self._frame_rate

    def reset(self):
        self._phase = 0
        self._state = 0

    def set_frequency(self, frequency):
        if frequency <= 0:
            raise pyx.ArgumentError(f"Frequency must be > 0, got {frequency}")

        self._p = self._frame_rate / frequency
        self._C2 = 1/self._p
        # self._rate = np.pi * self._C2
        self._rate = np.pi / self._p
        self.update_harmonics()
        # print(f'{frequency:.2f}, {self._p:.2f}, {self._C2:.4f}, {self._rate:.8f}')

    def set_harmonics(self, n_harmonics):
        self._n_harmonics = n_harmonics
        self.update_harmonics()
        self._state = -0.5 * self._a

    def update_harmonics(self):
        if self._n_harmonics == 0:
            max_harmonics = int(np.floor(0.5 * self._p))
            self._m = 2 * max_harmonics + 1
        else:
            self._m = 2 * self._n_harmonics + 1

        self._a = self._m / self._p
