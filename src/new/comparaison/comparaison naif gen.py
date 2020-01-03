from genetique.alg_gen2 import *
from naive.tsp1 import *
from common.distances import *

g5 = [City(x1, x2, n) \
      for x1, x2, n in
      [[0, 0, "O"], [10, 0, "A"], [10, 10, "B"], [0, 10, "C"], [5, 20, "D"]]]

def cnom(c):
    c_nom = []
    for k in range(len(c)):
        c_nom.append(c[k][2])
    return c_nom


def chemin_noms(chemin):
    return " -> ".join(c.nom for c in chemin) + ' ...'


cnom(g5)


def test():
    cgen, distgen = Dynamique_Population(g5, nb_gens=4, taille_pop=10, distfn=euclide)
    ctsp, disttsp = tsp1(g5, distfn=euclide)
    print('distance gen={0}, distance vraie = {1}'.format(distgen, disttsp))
    diff = (abs(disttsp - distgen) / disttsp)*100
    print('ecart relatif={0}'.format(diff))
    print('chemin gen: {0}, chemin vrai: {1}'.format(chemin_noms(cgen), chemin_noms(ctsp)))


 #Renvoie les distances de l'algo gen et de l'algo naif + les chemins associés

test()

