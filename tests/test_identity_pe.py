import os
import sys
script_dir = os.path.dirname( __file__ )
pygmu_dir = os.path.join( script_dir, '..', 'pygmu' )
sys.path.append( pygmu_dir )
import unittest
import numpy as np
from pygmu import (IdentityPE, Extent, PygPE)

class TestIdentityPE(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        self.pe = IdentityPE()
        self.assertIsInstance(self.pe, IdentityPE)

    def test_render(self):
        e = Extent(0, 5)
        self.pe = IdentityPE()
        expect = np.array([[0, 1, 2, 3, 4]], dtype=np.float32)
        got = self.pe.render(e)
        np.testing.assert_array_almost_equal(got, expect)

    def test_extent(self):
        self.pe = IdentityPE()
        self.assertTrue(Extent().equals(self.pe.extent()))

    def test_frame_rate(self):
        self.pe = IdentityPE()
        self.assertIsNone(self.pe.frame_rate())
        self.pe = IdentityPE(frame_rate=1234)
        self.assertEqual(self.pe.frame_rate(), 1234)

    def test_channel_count(self):
        self.pe = IdentityPE()
        self.assertEqual(self.pe.channel_count(), 1)

