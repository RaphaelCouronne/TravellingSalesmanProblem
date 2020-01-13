import unittest

import os

from os.path import dirname as dn
from common.tsplib import read_tsplib_path

class TSPTests(unittest.TestCase):

    def test_read_all_tsps(self):
        tsplibsd= os.path.join(dn(dn(__file__)), "tsplib")
        for tspf in os.listdir(tsplibsd):
            tspp = os.path.join(tsplibsd, tspf)
            print("-- reading tsplib file: {0}".format(tspp))
            g, d = read_tsplib_path(tspp)
            self.assertTrue(len(g) >= 3)

if __name__ == "__main__":
    unittest.main()
