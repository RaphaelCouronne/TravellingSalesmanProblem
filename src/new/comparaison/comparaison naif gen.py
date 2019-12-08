from genetique.alg_gen2 import *
from naive.tsp1 import *
from common.distances import *


def test():
    g5 = [City(x1, x2, n) \
          for x1, x2, n in
          [[0, 0, "O"], [10, 0, "A"], [10, 10, "B"], [0, 10, "C"], [5, 20, "D"]]]
    print(g5)
    cgen, distgen = Dynamique_Population(g5, nb_gens=4, taille_pop=10, distfn=euclide, gen_animation_fn=no_animation)
    ctsp, disttsp = tsp1(g5, distfn=euclide)
    print('* distance gen={0}, chemin gen={1}, distance vraie = {2}, chemin vrai = {3}'.format(distgen, cgen, disttsp, ctsp))
    #Renvoie les distances de l'algo gen et de l'algo naif + les chemins associés


if __name__ == "__main__":
    test()


