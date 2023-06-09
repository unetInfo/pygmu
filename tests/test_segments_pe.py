import unittest
import numpy as np
import os
import sys

script_dir = os.path.dirname( __file__ )
pygmu_dir = os.path.join( script_dir, '..', 'pygmu' )
sys.path.append( pygmu_dir )
import pyg_exceptions as pyx
from pygmu import (SegmentsPE, Extent, PygPE)

class TestSegmentsPE(unittest.TestCase):

    def setUp(self):
        self.tvs = np.array([[0, 1.0], [4, 2.0], [6, -3.0]], dtype=np.float32)
        self.pe_ramp = SegmentsPE(self.tvs, interpolation=SegmentsPE.RAMP)
        self.pe_step = SegmentsPE(self.tvs, interpolation=SegmentsPE.STEP)

    def test_init(self):
        self.assertIsInstance(self.pe_ramp, SegmentsPE)
        self.assertIsInstance(self.pe_step, SegmentsPE)

        with self.assertRaises(pyx.ArgumentError):
            # need at least 2 time / value pairs
            SegmentsPE(np.array([[0, 1]]))

    def test_insertion(self):
    	pe = SegmentsPE([[0, 100], [1, 200]])
    	np.testing.assert_array_almost_equal(pe._times, [0, 1])
    	np.testing.assert_array_almost_equal(pe._values, [100, 200])

    	# time order is maintained
    	pe = SegmentsPE([[1, 200], [0, 300]])
    	np.testing.assert_array_almost_equal(pe._times, [0, 1])
    	np.testing.assert_array_almost_equal(pe._values, [300, 200])

    	# duplicate times are ellided
    	pe = SegmentsPE([[0, 100], [1, 200], [1, 300]])
    	np.testing.assert_array_almost_equal(pe._times, [0, 1])
    	np.testing.assert_array_almost_equal(pe._values, [100, 300])

    	np.testing.assert_array_almost_equal(self.pe_ramp._times, [0, 4, 6])
    	np.testing.assert_array_almost_equal(self.pe_ramp._values, [1.0, 2.0, -3.0])

    def test_render(self):
        e = Extent(-5, 0)     # no overlap -- return first value
        expect = np.full([1, 5], 1.0, dtype=np.float32)
        got = self.pe_ramp.render(e)
        np.testing.assert_array_almost_equal(got, expect)
        got = self.pe_step.render(e)
        np.testing.assert_array_almost_equal(got, expect)

        e = Extent(6, 11)     # no overlap -- return last value
        expect = np.full([1, 5], -3.0, dtype=np.float32)
        got = self.pe_ramp.render(e)
        np.testing.assert_array_almost_equal(got, expect)
        got = self.pe_step.render(e)
        np.testing.assert_array_almost_equal(got, expect)

        e = Extent(-1, 8)
        # interpolation = ramp
        #           idx =  -1   0    1     2    3     4    5      6     7
        expect = np.array([1.0, 1.0, 1.25, 1.5, 1.75, 2.0, -0.5, -3.0, -3.0]).reshape(1, -1)
        got = self.pe_ramp.render(e)
        np.testing.assert_array_almost_equal(got, expect)

        # interpolation = step
        #           idx =  -1   0    1    2    3    4    5     6     7
        expect = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, -3.0, -3.0]).reshape(1, -1)
        got = self.pe_step.render(e)
        np.testing.assert_array_almost_equal(got, expect)

    def test_extent(self):
        self.assertTrue(Extent().equals(self.pe_ramp.extent()))
        self.assertTrue(Extent().equals(self.pe_step.extent()))

    def test_frame_rate(self):
        self.assertIsNone(self.pe_ramp.frame_rate())
        self.assertIsNone(self.pe_step.frame_rate())
        pe = SegmentsPE(self.tvs, frame_rate=1234)
        self.assertEqual(pe.frame_rate(), 1234)

    def test_channel_count(self):
        self.assertEqual(self.pe_ramp.channel_count(), 1)
        self.assertEqual(self.pe_step.channel_count(), 1)

