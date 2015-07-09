from bitarray import bitarray
from itertools import *
from timer import Timer
from random import *
from operator import itemgetter
from copy import *
from utils import *
import operator


import unittest


class TestListMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print 'x'

    def test_empty(self):
        self.assertEquals(0, len([]))
        self.assertNotEquals(0, len([42]))

    def test_append(self):
        self.assertTrue(isinstance([], list))
        self.assertFalse(issubclass(list, type), 'OMG')

    @unittest.skip('bad')
    def test_remove(self):
        self.assertRaises(ValueError, [].remove, 42)
        with self.assertRaises(ValueError):
            [].remove(42)

    @unittest.expectedFailure
    def test_fail(self):
        self.assertEquals(1, 1)

    # def setUp(self):
    #     pass

    # def tearDown(self):
    #     pass




class X_Test(unittest.TestCase):
    def runTest(self):
        print 'sad'
        self.assertEqual(True, False)

# unittest.main()
#



suite = unittest.TestLoader().loadTestsFromTestCase(TestListMethods)
unittest.TextTestRunner(verbosity=2).run(suite)

# print unittest.TestLoader().discover('cover_sort')