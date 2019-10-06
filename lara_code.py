# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:20:17 2019

@author: Lara
"""

from random import *
import time

import math
from random import *
from pylab import *

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


    
    #Algorithme génétique
    
    
from random import *
from pylab import *

def Poids_Arete(M,N):
    return sqrt((M[0]-N[0])**2+(M[1]-N[1])**2)
#calcule la norme. Un individu correspond a une liste de villes (coordonnées) dans un ordre donné ; c'est un trajet

def Adaptation_Individu(villes_distances, individu) :
    poids = 0
    ville_debut = len(individu) # on commence à la derniere ville
    ville_actuelle = ville_debut
    for ville_indice in individu:
        poids += villes_distances[ville_actuelle][ville_indice]
        ville_actuelle = ville_indice
    return poids + villes_distances[ville_actuelle][ville_debut] # on boucle le cycle
#calcule le "poids" d'un individu, à savoir à quel point il est adapté. Plus ce nombre est faible, plus il est adapté au problème



def Hybridation(individu1,individu2,i) :
    Liste1,Liste2=individu1.copy(),individu2.copy()
    n=len(Liste1)
    return [Liste1[:i]+[x for x in Liste2 if Liste1[:i].count(x)==0], Liste2[:i]+[x for x in Liste1 if Liste2[:i].count(x)==0]]
#hybride 2 individus. On prend le premier jusqu'à i, puis on complète avec le second en vérifiant qu'aucun élément (= ville) ne se répète

def alea_hybridation(individu1, individu2):
    Liste1, Liste2 = individu1.copy(), individu2.copy()
    n = len(Liste1)
    return Hybridation(individu1, individu2, randint(1, n))
#hybride 2 individus aléatoirement

##Mutation ? 



def selection_tournoi(villes_distances, individu1, individu2) :
    poids1, poids2 = Adaptation_Individu(villes_distances,individu1), Adaptation_Individu(villes_distances, individu2)

    if poids1 <= poids2:
        return individu1
    else:
        return individu2
    #renvoie l'individu le plus adapté

def deux_adversaires_alea(population) :
    n = len(population)
    k,l = 0, 0
    if n==1:
        raise ValueError("Ne peux pas generer 2 individus d une population de 1")
    while k==l:
        k, l = randint(0,n), randint(0,n)
    return population[k], population[l]
#la population est une liste de liste. On en renvoie deux individus distincts ; on retire k pour être sûr de ne pas prendre deux fois le même individu


def compute_poid_population(villes_distances, population):
    sum=0
    for individu in population:
        sum += Adaptation_Individu(villes_distances, individu)

    return sum

def meilleure_moitie(villes_distances, population):
    n = len(population)
    Liste_adaptation = [Adaptation_Individu(villes_distances, x) for x in population]
    Liste_adaptation.sort() #on classe dans l'ordre croissant
    Liste_Meilleurs = [] #vide pour l'instant
    Mediane = Liste_adaptation[n//2]
    for individu in population:
        if Adaptation_Individu(villes_distances, individu) <= Mediane :
            Liste_Meilleurs.append(individu)

    while len(Liste_Meilleurs) != n//2 :
        Liste_Meilleurs.remove(Liste_Meilleurs[-1]) # on élimine un individu de la médiane

    return Liste_Meilleurs


def meilleur_individu(villes_distances, population):
    n = len(population)

    individu = population[0]
    meilleur = individu
    min_adaptation = Adaptation_Individu(villes_distances, individu)

    for individu in population:
        adaptation = Adaptation_Individu(villes_distances, individu)
        if adaptation < min_adaptation:
            meilleur = individu
            min_adaptation = adaptation

    return meilleur, min_adaptation

def generation_suivante(villes_distances, population):
    n = len(population)
    population_Temp = []
    for k in range(n):
        individu1, individu2 = deux_adversaires_alea(population)
        gagnant = selection_tournoi(villes_distances, individu1, individu2)
        population_Temp.append(gagnant)
    for k in range(n-1) :
        for l in range(n-1-k) :
            x = uniform(0,1)
            if x < 0.2 :
                population_Temp[k], population_Temp[l+k+1] = alea_hybridation(population_Temp[k], population_Temp[l+k+1])
#On remplace les individus d'avant par ceux hybridés
    return meilleure_moitie(villes_distances, population_Temp) + meilleure_moitie(villes_distances, population)

def calcul_distances(villes):
    """
    Retourne la matrice de distance entre les villes
    :param villes:
    :return:
    """

    n_villes = len(villes)

    villes_distances = []

    for i in range(n_villes):
        villes_distances.append([])
        for j in range(n_villes):
            # Calcul de la distance entre 2 sommets
            dist = distance_euclide(villes[i], villes[j])
            villes_distances[i].append(dist)
    return villes_distances

def fact(n):
    """fact(n): calcule la factorielle de n (entier >= 0)"""
    if n<2:
        return 1
    else:
        return n*fact(n-1)

def generate_random_permutation(n):

    l=[]
    longueur=0

    while longueur<n:
        entier_proposition = randint(n)
        if entier_proposition not in l:
            l.append(entier_proposition)
            longueur += 1

    return l
    
def test_gen(villes, n_iterations, n_samples):

    # Initialisation
    #liste_trajets = Liste_Permutees(len(villes)) tres long !!!
    #population = [liste_trajets[idx] for idx in [randint(0, fact(len(villes)-1)) for i in range(n_genetic)]]

    population = [generate_random_permutation(len(villes)-1) for i in range(n_samples)]

    villes_distances = calcul_distances(villes)

    best_list = []

    # Boucle sur n fois nouvelle generation
    for k in range(n_iterations):
        population = generation_suivante(villes_distances, population)
        best = meilleur_individu(villes_distances, population)[1]
        best_list.append(best)
        print("Iteration :",k, " Best : ", best)
        print("Energie : ",[Adaptation_Individu(villes_distances, individu) for individu in population])
        # Sortir si pas mieux les 10 dernieres iterations
        if k > 20:
            list_mieux = [best-lastbest for lastbest in best_list[-50:] if best-lastbest<0]
            if len(list_mieux)==0:
                print("Arreter car on fait pas mieux")
                break
    return meilleur_individu(villes_distances, population)
    
def test(n, max):
    liste_ville = []
    for k in range(n):
        a, b = randint(0,max), randint(0, max)
        liste_ville.append([a,b])
    return liste_ville
    
test1 = [[38, 97], [32, 47], [9, 59], [21, 74], [63, 35], [49, 78]]

#Quand je fais "test_gen(test1, 3), ça me donne une erreur que je ne comprends pas... 