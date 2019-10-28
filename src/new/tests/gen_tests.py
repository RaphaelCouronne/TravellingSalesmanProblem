from genetique.alg_gen2 import *

from common.distances import *

import unittest

# Liste_Sommets1 = [[1, 2], [5, 4], [6, 2], [3, 2], [5, 3], [1, 6]]
# Population = Generation_Pop_Alea(Liste_Sommets1, 4)
# print(Generation_Suivante(Population)) # pas d'erreur de syntaxe ...

class HybridationTests(unittest.TestCase):

    def test_hybridation4(self):
        c1 = [1,2,3,4]
        c2 = [2,4,3,1]
        h1, h2 = Hybridation(c1, c2, 1)
        self.assertEqual([1,2,4,3], h1)
        self.assertEqual([2,1,3,4], h2)

    def test_hybrid10(self):
        c1 = list(range(10))
        c2 = [0, 4, 1, 6, 3, 9, 8, 2, 5, 7]
        h1, h2 = Hybridation(c1, c2, 5)
        self.assertEqual([0,1,2,3,4,6,9,8,5,7], h1)
        self.assertEqual([0,4,1,6,3,2,5,7,8,9], h2)
        j1, j2 = Hybridation(c1, c2, 3)
        self.assertEqual([0,1,2,4,6,3,9,8,5,7], j1)
        self.assertEqual([0,4,1,2,3,5,6,7,8,9], j2)


    def test_g9(self):
        g9 = [City(1, x2, "city_%d" % c) \
              for c, (x1, x2) in
              enumerate([[0, 0], [100, 100], [0, 100], [100, 0], [50, 50], [75, 15], [75, 35], [20, 40], [50, 20]])]



    def test_plus_court_trajets(self):
        g4 = [City(x1, x2, "city_%d" % c) \
              for c, (x1, x2) in
              enumerate([[0, 0], [100, 100], [0, 101], [102, 0]])]
        ipct = Individu_Plus_Courts_Trajets(g4, 0, distfn=manhattan)
        x1s = [v.x1 for v in ipct]
        x2s = [v.x2 for v in ipct]
        self.assertEqual([0, 0, 100, 102], x1s)
        self.assertEqual([0, 101, 100, 0], x2s)


if __name__ == '__main__':
    unittest.main()