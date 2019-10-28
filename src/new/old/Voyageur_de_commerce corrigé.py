#from pylab import *

from matplotlib.pylab import *
import matplotlib.pylab
__doc__ = matplotlib.pylab.__doc__

## Question 1) 

# Compter le nombre de cycles hamiltoniens,
# sans pour l'instant faire la confusion entre deux trajectoires gloabelement identiques,
# revient à choisir un premier sommet, puis un autre, etc. ce qui fait n! choix.
# Ensuite, pour une même trajectoire globale, il existe exactement n cycles hamiltoniens
# parcourus dans un sens et n cycles hamiltoniens décrits dans le sens inverse,
# cela provenant tout simplement du choix du point de départ dans le cycle.
# En définitive, il y a exactement (n-1)!/2 trajectoires hamiltoniennes dans un graphe à n sommets.

## Question 2)


# D'autre part, pour chaque trajectoire hamiltonienne,
# il faut compter la somme des poids, ce qui fait un nombre d'opérations en O(n).
# Au final, pour déterminer le minimum sur les trajectoires hamiltoniennes pondérées
# et en détecter la trajectoire optimale, il faut effecteur un nombre d'opérations
# en O(n!), ce qui est énorme !!!


## Question 3)

# n = nombre de sommets du graphe complet

from common import *
import time


def Sommets_Graphe_Alea(n):
    """ détermine les sommets aléatoires par la loi uniforme sur le carré [0,100]**2
    """
    return [[uniform(0, 100), uniform(0, 100)] for _ in range(n)]

# print(Sommets_Graphe_Alea(4)) # test OK

def Poids_Arete(M, N):
    """ calcule le poids associé à l'arête  {M,N} """
    return sqrt((M[0] - N[0]) ** 2 + (M[1] - N[1]) ** 2)


# print(Poids_Arete([1,2],[4,-1])) # test OK

def Liste_Permutees(n):
    """ retourne la liste des listes obtenues à
        partir de range(n-1) en permutant les occurrences
    """
    print("--> entre dans permut n={0}".format(n))
    if n == 2:
        print("<-- sortie de permut n={0}, p={1}".format(n, [[0]]))
        return [[0]]
    else:
        Liste_Temp = []
        prec = Liste_Permutees(n - 1)
        for L in prec:  # on le fait par récursivité !!!
            for k in range(n - 2):
                Liste_L = L.copy()  # pour le pas modifier la liste L
                Liste_L.insert(k, n - 2)  # on insère en place k l'entier n
                Liste_Temp.append(Liste_L)  # on met en mémoire
            Liste_Temp.append(L + [n - 2])  # on rajoute la liste où n est en dernière position
        print("<-- sortie de permut n={0}, p={1}".format(n, Liste_Temp))
        return Liste_Temp


# print(Liste_Permutees(5)) # tests OK

def Poids_Trajectoire(Liste_Sommets):
    """ calcule le poids affecté à une chaîne de sommets """
    n = len(Liste_Sommets)
    Poids_Temp = 0
    for k in range(n - 1):
        Poids_Temp += Poids_Arete(Liste_Sommets[k], Liste_Sommets[k + 1])
    return Poids_Temp + Poids_Arete(Liste_Sommets[-1], Liste_Sommets[0])  # pour boucler le cycle


# print(Poids_Trajectoire(Sommets_Graphe_Alea(n))) # test OK

def Algorithme_Voyageur_De_Commerce(Sommets):
    """ implémente l'algorithme de recherche de la trajectoire minimale en comparant tous les chemins """
    n = len(Sommets)
    Premier_Sommet, Sommets_Suivants = Sommets[0], Sommets[1:]
    Poids_Trajectoire_Mini = Poids_Trajectoire(Sommets)
    Chemin_Mini = Sommets
    for Liste in Liste_Permutees(n):
        Poids_Chemin = Poids_Trajectoire([Premier_Sommet] + [Sommets_Suivants[k] for k in Liste])
        if Poids_Chemin < Poids_Trajectoire_Mini:
            Poids_Trajectoire_Mini = Poids_Chemin
            Chemin_Mini = [Premier_Sommet] + [Sommets_Suivants[k] for k in Liste]

    figure()
    axis([-10, 110, -10, 110])
    plot([Sommets[k][0] for k in range(n)], [Sommets[k][1] for k in range(n)], color="red", linestyle="-", marker="s")
    plot([Chemin_Mini[k][0] for k in range(n)] + [Chemin_Mini[0][0]],
         [Chemin_Mini[k][1] for k in range(n)] + [Chemin_Mini[0][1]], color="blue", linestyle="-")
    show()


#Algorithme_Voyageur_De_Commerce(Sommets_Graphe_Alea(8)) # tests OK

Graphe = [[0, 0], [100, 100], [0, 100], [100, 0], [50, 50], [75, 15], [75, 35], [20, 40], [50, 20]]


# for k in range(len(Graphe)-1) :
#    Algorithme_Voyageur_De_Commerce(Graphe[:k+2]) # tests OK

def Algorithme_Voyageur_De_Commerce_Calcul_Temps(Sommets):
    """ calcule le temps d'exécution """

    n = len(Sommets)
    ## la résolution commence vraiment ici ##
    t_0 = time.clock()
    Premier_Sommet, Sommets_Suivants = Sommets[0], Sommets[1:]
    Poids_Trajectoire_Mini = Poids_Trajectoire(Sommets)
    Chemin_Mini = Sommets
    for Liste in Liste_Permutees(n):
        Poids_Chemin = Poids_Trajectoire([Premier_Sommet] + [Sommets_Suivants[k] for k in Liste])
        if Poids_Chemin < Poids_Trajectoire_Mini:
            Poids_Trajectoire_Mini = Poids_Chemin
            Chemin_Mini = [Premier_Sommet] + [Sommets_Suivants[k] for k in Liste]
    t_1 = time.clock()
    ## fin de la résolution ##

    return t_1 - t_0  # temps d'exécution


# print(Algorithme_Voyageur_De_Commerce_Calcul_Temps(Sommets_Graphe_Alea(7))) # tests OK

# Qustion 4) 

# def Traces_Temps_Execution(p):
#     """ trace la suite des temps de calcul """
#     figure()
#     X = [k + 2 for k in range(p)]
#     Y = [Algorithme_Voyageur_De_Commerce_Calcul_Temps(Sommets_Graphe_Alea(k)) for k in X]
#     Z = [log(y) for y in Y]  # échelle logarithmique en ordonnées
#     plot(X, Z, color="red", marker="o", linestyle="-")
#     show()


#Traces_Temps_Execution(9)


# Les temps d'exécution sont bien conformes à la théorie, car en échelle logarithmique en ordonnées, on a une courbe encore convexe.

# Nous définissons la fonction Factorielle par récursivité :

def Factorielle(p):
    if p == 0:
        return 1
    else:
        return p * Factorielle(p - 1)

# temps de calcul pour 17 villes :
# print(Factorielle(17)/(1e6*3600*24*365)) # Un peu plus de 11 années d'exécution pour 17 villes !!!


# temps de calcul pour 24 villes :
# print(Factorielle(24)/(1e6*3600*24*365)) # Plus de 19,6 milliards d'années pour 24 villes !!!


# print(Liste_Permutees(4))
# Algorithme_Voyageur_De_Commerce(Sommets_Graphe_Alea(8)) # tests OK