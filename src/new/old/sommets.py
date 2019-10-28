from common import uniform

import math

def sommets_graphe_aleatoire(nb, taille=100):
    # retourne nb sommets aleatoires dans une grille de taille `taille` (defaut 100)
    return [ (uniform(0, taille), uniform(0, taille)) for _ in range(nb)]

def distance_euclide(sommet1, sommet2):
    # distance euclidienne
    # les sommets sont des tuples (x,y)
    x1, y1 = sommet1
    x2, y2 = sommet2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def Poids_Trajectoire(sommets, distfn=distance_euclide):
    """ calcule le poids affecté à une chaîne de sommets """
    nb_sommets = len(sommets)
    Poids_Temp = 0
    for k in range(nb_sommets - 1):
        Poids_Temp += distfn(sommets[k], sommets[k + 1])
    return Poids_Temp + distfn(sommets[-1], sommets[0])  # pour boucler le cycle
