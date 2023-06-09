import os
import sys
import unittest
import numpy as np
import math
script_dir = os.path.dirname( __file__ )
pygmu_dir = os.path.join( script_dir, '..', 'pygmu' )
sys.path.append( pygmu_dir )
from pygmu import (Extent)
class TestExtent(unittest.TestCase):

    def test_constructors(self):
        a0 = Extent()
        a1 = Extent(start=10)
        a2 = Extent(end=100)
        a3 = Extent(start=10, end=100)
        self.assertEqual(a0.start(), Extent.NINF)
        self.assertEqual(a0.end(), Extent.PINF)
        self.assertEqual(a1.start(), 10)
        self.assertEqual(a1.end(), Extent.PINF)
        self.assertEqual(a2.start(), Extent.NINF)
        self.assertEqual(a2.end(), 100)
        self.assertEqual(a3.start(), 10)
        self.assertEqual(a3.end(), 100)

    def test_is_indefinite(self):
        a0 = Extent()
        a1 = Extent(start=10)
        a2 = Extent(end=100)
        a3 = Extent(start=10, end=100)
        self.assertTrue(a0.is_indefinite())
        self.assertTrue(a1.is_indefinite())
        self.assertTrue(a2.is_indefinite())
        self.assertFalse(a3.is_indefinite())

    def test_duration(self):
        a0 = Extent()
        a1 = Extent(start=10)
        a2 = Extent(end=100)
        a3 = Extent(start=10, end=100)
        self.assertTrue(math.isinf(a0.duration()))
        self.assertTrue(math.isinf(a1.duration()))
        self.assertTrue(math.isinf(a2.duration()))
        self.assertEqual(a3.duration(), 90)

    def test_offset(self):
        a0 = Extent().offset(20)
        a1 = Extent(start=10).offset(20)
        a2 = Extent(end=100).offset(20)
        a3 = Extent(start=10, end=100).offset(20)
        self.assertEqual(a0.start(), Extent.NINF)
        self.assertEqual(a0.end(), Extent.PINF)
        self.assertEqual(a1.start(), 30)
        self.assertEqual(a1.end(), Extent.PINF)
        self.assertEqual(a2.start(), Extent.NINF)
        self.assertEqual(a2.end(), 120)
        self.assertEqual(a3.start(), 30)
        self.assertEqual(a3.end(), 120)

    def test_precedes(self):
        a0 = Extent(end=10)
        a1 = Extent(start=0, end=20)
        a2 = Extent(start=10, end=30)
        a3 = Extent(start=20, end=40)
        a4 = Extent(start=30)
        self.assertFalse(a0.precedes(a0))
        self.assertFalse(a0.precedes(a1))
        self.assertTrue(a0.precedes(a2))
        self.assertTrue(a0.precedes(a3))
        self.assertTrue(a0.precedes(a4))

        self.assertFalse(a1.precedes(a0))
        self.assertFalse(a1.precedes(a1))
        self.assertFalse(a1.precedes(a2))
        self.assertTrue(a1.precedes(a3))
        self.assertTrue(a1.precedes(a4))

        self.assertFalse(a2.precedes(a0))
        self.assertFalse(a2.precedes(a1))
        self.assertFalse(a2.precedes(a2))
        self.assertFalse(a2.precedes(a3))
        self.assertTrue(a2.precedes(a4))

        self.assertFalse(a3.precedes(a0))
        self.assertFalse(a3.precedes(a1))
        self.assertFalse(a3.precedes(a2))
        self.assertFalse(a3.precedes(a3))
        self.assertFalse(a3.precedes(a4))

        self.assertFalse(a4.precedes(a0))
        self.assertFalse(a4.precedes(a1))
        self.assertFalse(a4.precedes(a2))
        self.assertFalse(a4.precedes(a3))
        self.assertFalse(a4.precedes(a4))

        self.assertFalse(a0.precedes(0))
        self.assertTrue(a0.precedes(10))
        self.assertTrue(a0.precedes(20))
        self.assertTrue(a0.precedes(30))
        self.assertTrue(a0.precedes(40))

        self.assertFalse(a1.precedes(0))
        self.assertFalse(a1.precedes(10))
        self.assertTrue(a1.precedes(20))
        self.assertTrue(a1.precedes(30))
        self.assertTrue(a1.precedes(40))

        self.assertFalse(a2.precedes(0))
        self.assertFalse(a2.precedes(10))
        self.assertFalse(a2.precedes(20))
        self.assertTrue(a2.precedes(30))
        self.assertTrue(a2.precedes(40))

        self.assertFalse(a3.precedes(0))
        self.assertFalse(a3.precedes(10))
        self.assertFalse(a3.precedes(20))
        self.assertFalse(a3.precedes(30))
        self.assertTrue(a3.precedes(40))

        self.assertFalse(a4.precedes(0))
        self.assertFalse(a4.precedes(10))
        self.assertFalse(a4.precedes(20))
        self.assertFalse(a4.precedes(30))
        self.assertFalse(a4.precedes(40))

    def test_follows(self):
        a0 = Extent(end=10)
        a1 = Extent(start=0, end=20)
        a2 = Extent(start=10, end=30)
        a3 = Extent(start=20, end=40)
        a4 = Extent(start=30)
        self.assertFalse(a0.follows(a0))
        self.assertFalse(a0.follows(a1))
        self.assertFalse(a0.follows(a2))
        self.assertFalse(a0.follows(a3))
        self.assertFalse(a0.follows(a4))

        self.assertFalse(a1.follows(a0))
        self.assertFalse(a1.follows(a1))
        self.assertFalse(a1.follows(a2))
        self.assertFalse(a1.follows(a3))
        self.assertFalse(a1.follows(a4))

        self.assertTrue(a2.follows(a0))
        self.assertFalse(a2.follows(a1))
        self.assertFalse(a2.follows(a2))
        self.assertFalse(a2.follows(a3))
        self.assertFalse(a2.follows(a4))

        self.assertTrue(a3.follows(a0))
        self.assertTrue(a3.follows(a1))
        self.assertFalse(a3.follows(a2))
        self.assertFalse(a3.follows(a3))
        self.assertFalse(a3.follows(a4))

        self.assertTrue(a4.follows(a0))
        self.assertTrue(a4.follows(a1))
        self.assertTrue(a4.follows(a2))
        self.assertFalse(a4.follows(a3))
        self.assertFalse(a4.follows(a4))

        self.assertFalse(a0.follows(0))
        self.assertFalse(a0.follows(10))
        self.assertFalse(a0.follows(20))
        self.assertFalse(a0.follows(30))
        self.assertFalse(a0.follows(40))

        self.assertFalse(a1.follows(0))
        self.assertFalse(a1.follows(10))
        self.assertFalse(a1.follows(20))
        self.assertFalse(a1.follows(30))
        self.assertFalse(a1.follows(40))

        self.assertTrue(a2.follows(0))
        self.assertFalse(a2.follows(10))
        self.assertFalse(a2.follows(20))
        self.assertFalse(a2.follows(30))
        self.assertFalse(a2.follows(40))

        self.assertTrue(a3.follows(0))
        self.assertTrue(a3.follows(10))
        self.assertFalse(a3.follows(20))
        self.assertFalse(a3.follows(30))
        self.assertFalse(a3.follows(40))

        self.assertTrue(a4.follows(0))
        self.assertTrue(a4.follows(10))
        self.assertTrue(a4.follows(20))
        self.assertFalse(a4.follows(30))
        self.assertFalse(a4.follows(40))

    def test_overlaps(self):
        a0 = Extent(end=10)
        a1 = Extent(start=0, end=20)
        a2 = Extent(start=10, end=30)
        a3 = Extent(start=20, end=40)
        a4 = Extent(start=30)
        self.assertTrue(a0.overlaps(a0))
        self.assertTrue(a0.overlaps(a1))
        self.assertFalse(a0.overlaps(a2))
        self.assertFalse(a0.overlaps(a3))
        self.assertFalse(a0.overlaps(a4))

        self.assertTrue(a1.overlaps(a0))
        self.assertTrue(a1.overlaps(a1))
        self.assertTrue(a1.overlaps(a2))
        self.assertFalse(a1.overlaps(a3))
        self.assertFalse(a1.overlaps(a4))

        self.assertFalse(a2.overlaps(a0))
        self.assertTrue(a2.overlaps(a1))
        self.assertTrue(a2.overlaps(a2))
        self.assertTrue(a2.overlaps(a3))
        self.assertFalse(a2.overlaps(a4))

        self.assertFalse(a3.overlaps(a0))
        self.assertFalse(a3.overlaps(a1))
        self.assertTrue(a3.overlaps(a2))
        self.assertTrue(a3.overlaps(a3))
        self.assertTrue(a3.overlaps(a4))

        self.assertFalse(a4.overlaps(a0))
        self.assertFalse(a4.overlaps(a1))
        self.assertFalse(a4.overlaps(a2))
        self.assertTrue(a4.overlaps(a3))
        self.assertTrue(a4.overlaps(a4))

        self.assertTrue(a0.overlaps(0))
        self.assertFalse(a0.overlaps(10))
        self.assertFalse(a0.overlaps(20))
        self.assertFalse(a0.overlaps(30))
        self.assertFalse(a0.overlaps(40))

        self.assertTrue(a1.overlaps(0))
        self.assertTrue(a1.overlaps(10))
        self.assertFalse(a1.overlaps(20))
        self.assertFalse(a1.overlaps(30))
        self.assertFalse(a1.overlaps(40))

        self.assertFalse(a2.overlaps(0))
        self.assertTrue(a2.overlaps(10))
        self.assertTrue(a2.overlaps(20))
        self.assertFalse(a2.overlaps(30))
        self.assertFalse(a2.overlaps(40))

        self.assertFalse(a3.overlaps(0))
        self.assertFalse(a3.overlaps(10))
        self.assertTrue(a3.overlaps(20))
        self.assertTrue(a3.overlaps(30))
        self.assertFalse(a3.overlaps(40))

        self.assertFalse(a4.overlaps(0))
        self.assertFalse(a4.overlaps(10))
        self.assertFalse(a4.overlaps(20))
        self.assertTrue(a4.overlaps(30))
        self.assertTrue(a4.overlaps(40))

    def test_spans(self):
        a0 = Extent()
        a1 = Extent(start=10, end=40)
        a2 = Extent(start=0, end=20)
        a3 = Extent(start=20, end=30)

        self.assertTrue(a0.spans(a0))
        self.assertTrue(a0.spans(a1))
        self.assertTrue(a0.spans(a2))
        self.assertTrue(a0.spans(a3))

        self.assertFalse(a1.spans(a0))
        self.assertTrue(a1.spans(a1))
        self.assertFalse(a1.spans(a2))
        self.assertTrue(a1.spans(a3))

        self.assertFalse(a2.spans(a0))
        self.assertFalse(a2.spans(a1))
        self.assertTrue(a2.spans(a2))
        self.assertFalse(a2.spans(a3))

        self.assertFalse(a3.spans(a0))
        self.assertFalse(a3.spans(a1))
        self.assertFalse(a3.spans(a2))
        self.assertTrue(a3.spans(a3))

        self.assertTrue(a0.spans(0))
        self.assertTrue(a0.spans(10))
        self.assertTrue(a0.spans(20))
        self.assertTrue(a0.spans(30))
        self.assertTrue(a0.spans(40))

        self.assertFalse(a1.spans(0))
        self.assertTrue(a1.spans(10))
        self.assertTrue(a1.spans(20))
        self.assertTrue(a1.spans(30))
        self.assertFalse(a1.spans(40))

        self.assertTrue(a2.spans(0))
        self.assertTrue(a2.spans(10))
        self.assertFalse(a2.spans(20))
        self.assertFalse(a2.spans(30))
        self.assertFalse(a2.spans(40))

        self.assertFalse(a3.spans(0))
        self.assertFalse(a3.spans(10))
        self.assertTrue(a3.spans(20))
        self.assertFalse(a3.spans(30))
        self.assertFalse(a3.spans(40))

    def test_union(self):
        a0 = Extent()
        a1 = Extent(start=0, end=10)
        a2 = Extent(start=20, end=30)

        self.assertTrue(a0.equals(a0.union(a0)))
        self.assertTrue(a0.equals(a0.union(a1)))
        self.assertTrue(a0.equals(a0.union(a2)))

        self.assertTrue(a0.equals(a1.union(a0)))
        self.assertTrue(a1.equals(a1.union(a1)))
        self.assertTrue(Extent(start=0, end=30).equals(a1.union(a2)))

        self.assertTrue(a0.equals(a2.union(a0)))
        self.assertTrue(Extent(start=0, end=30).equals(a2.union(a1)))
        self.assertTrue(a2.equals(a2.union(a2)))

    def test_intersect(self):
        a0 = Extent()
        a1 = Extent(start=0, end=10)
        a2 = Extent(start=20, end=30)

        self.assertTrue(a0.equals(a0.intersect(a0)))
        self.assertTrue(a1.equals(a0.intersect(a1)))
        self.assertTrue(a2.equals(a0.intersect(a2)))

        self.assertTrue(a1.equals(a1.intersect(a0)))
        self.assertTrue(a1.equals(a1.intersect(a1)))
        self.assertTrue(a1.intersect(a2).is_empty())

        self.assertTrue(a2.equals(a2.intersect(a0)))
        self.assertTrue(a2.intersect(a1).is_empty())
        self.assertTrue(a2.equals(a2.intersect(a2)))

    def test_repr(self):
        self.assertIsInstance(Extent().__repr__(), str)
