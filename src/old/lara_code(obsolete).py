# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:20:17 2019

@author: Lara
"""

from random import *
import time

import math

import math # pour sqrt
def distance_euclide(sommet1, sommet2):
    # distance euclidienne
    # les sommets sont des tuples (x,y)
    x1, y1 = sommet1
    x2, y2 = sommet2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def distance_chemin(sommets, distfn=distance_euclide):
    """ calcule le poids affecté à une chaîne de sommets """
    nb_sommets = len(sommets)
    Poids_Temp = 0
    for k in range(nb_sommets - 1):
        Poids_Temp += distfn(sommets[k], sommets[k + 1])
    return Poids_Temp + distfn(sommets[-1], sommets[0])  # pour boucler le cycle

def Liste_Permutees(n):
    # n est un nombre de sommets
    # on retourne les permutations des n-1 suivants.
    verbose = False
    if verbose:
        print("--> entre dans permut n={0}".format(n))
    if n == 2:
        if verbose:
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
        if verbose:
            print("<-- sortie de permut n={0}, p={1}".format(n, Liste_Temp))
        return Liste_Temp


def tsp1(sommets):
    """ implémente l'algorithme de recherche de la trajectoire minimale
    en comparant tous les chemins """
    nb_sommets = len(sommets)
    # on calcule une distance initiale
    Premier_Sommet, sommets_Suivants = sommets[0], sommets[1:]
    distance_mini = distance_chemin(sommets)
    chemin_mini = sommets

    for Liste in Liste_Permutees(nb_sommets):
        chemin_possible = [Premier_Sommet] + [sommets_Suivants[k] for k in Liste]
        Poids_Chemin = distance_chemin(chemin_possible)
        if Poids_Chemin < distance_mini:
            distance_mini = Poids_Chemin
            chemin_mini = chemin_possible
    # on retourne un tuple: liste de N sommets (le chemin) + la distance (un nombre)
    return chemin_mini, distance_mini

from random import uniform

def sommets_graphe_aleatoire(nb, taille=100):
    # retourne nb sommets aleatoires dans une grille de taille `taille` (defaut 100)
    return [ (uniform(0, taille), uniform(0, taille)) for _ in range(nb)]
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not found. essayer 'pip install matplotlib'")


def print_graphe(Sommets, chemin_mini=None, taille=100):
    import matplotlib.pyplot as plt

    def plot_arrow(s1, s2, color, f=.5):
        x0, y0 = s1
        x1, y1 = s2
        line = plt.plot([x0, x1], [y0, y1], color=color)

        f = max(f, .0001)
        dx = f * (x1 - x0)
        dy = f * (y1 - y0)
        a = plt.arrow(x0, y0, dx, dy,
                      color=color, head_width=5, head_length=6)

    plt.figure(figsize=(10, 6))
    marge = 10
    plt.axis([-marge, taille + marge, -marge, taille + marge])

    plt.scatter([s[0] for s in Sommets], [s[1] for s in Sommets], s=100, color="red", marker="s")
    nb_sommets = len(Sommets)

    # le chemin affiche est soit le mini soit le Sommets initial
    chemin = chemin_mini or Sommets

    for k in range(nb_sommets - 1):
        plot_arrow(chemin[k], chemin[k + 1], color='blue')
    plot_arrow(chemin[-1], chemin[0], color='blue')
    # plt.plot([Chemin_Mini[k][0] for k in range(nb_sommets)] + [Chemin_Mini[0][0]],
    #          [Chemin_Mini[k][1] for k in range(nb_sommets)] + [Chemin_Mini[0][1]],
    #          color="blue", linestyle="-")

    plt.show()
import time

def chrono_tsp1(Sommets):
    print('-> start chrono tsp, nb sommets={0}'.format(len(Sommets)))
    t1 = time.clock()
    chemin, distance = tsp1(Sommets)
    t2 = time.clock()
    print('<- end chrono tsp, nb sommets={0}, time={1}'.format(len(Sommets), (t2-t1)))
    return (t2-t1), chemin, distance


def calcule_tsp(p):
    X = [k + 2 for k in range(p)]
    Y = [chrono_tsp1(sommets_graphe_aleatoire(k))[0] for k in X]
    Z = list(map(math.log, Y))  # échelle logarithmique en ordonnées
    return X, Y, Z


def plot_times(X, Y, Z):
    import matplotlib.pyplot as plt
    """ trace la suite des temps de calcul """
    plt.figure()
    # nb de points
    plt.plot(X, Z, color="green", marker="o", linestyle="-")
    plt.show()


def rendement(u):
    chemin, distance = tsp1(u)
    return (distance_chemin(u)) / distance


def graph_rendement(u):
    X = [k + 2 for k in range(u)]
    Y = [rendement(sommets_graphe_aleatoire(k)) for k in X]
    plt.plot(X, Y, color="blue", marker="o", linestyle="-")
    plt.show()


#Test


#On code une fonction adaptée

def voyageurmernoire (Villes):
    liste_trajets = Liste_Permutees (len(Villes))
    vrailiste_trajets = []
    for i in range (len(liste_trajets)):
        if ([liste_trajets[i][0], liste_trajets[i][-1]] == [0, 1] ) or ([liste_trajets[i][0], liste_trajets[i][-1]] == [1, 0]):
            vrailiste_trajets.append (liste_trajets [i])
            #On ne garde que les trajets qui bouclent
    meilleur = vrailiste_trajets [0]
    distancemin = distancemernoire (meilleur)
       
    for k in range (1,len(vrailiste_trajets)):
        dist = distancemernoire (vrailiste_trajets[k])
        if dist < distancemin:
            meilleur = vrailiste_trajets[k]
            distancemin = dist
    ordre = [NomVilles [k] for k in meilleur]
    return distancemin, ordre

