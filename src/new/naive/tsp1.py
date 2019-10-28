from common.distances import euclide, distance_chemin, City, manhattan


def Liste_Permutees(n):
    """ retourne les permutations"""
    verbose = True
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
                Liste_L.insert(k, n - 2)    # on insère en place k l'entier n
                Liste_Temp.append(Liste_L)  # on met en mémoire
            Liste_Temp.append(L + [n - 2])  # on rajoute la liste où n est en dernière position
        if verbose:
            print("<-- sortie de permut n={0}, p={1}".format(n, Liste_Temp))
        return Liste_Temp


def tsp1(Sommets, distfn=euclide):
    """ implémente l'algorithme de recherche de la trajectoire minimale en comparant tous les chemins """
    nb_sommets = len(Sommets)
    # on calcule une distance initiale
    Premier_Sommet, Sommets_Suivants = Sommets[0], Sommets[1:]
    Poids_Trajectoire_Mini = distance_chemin(Sommets, distfn)
    Chemin_Mini = Sommets

    for Liste in Liste_Permutees(nb_sommets):
        Poids_Chemin = distance_chemin([Premier_Sommet] + [Sommets_Suivants[k] for k in Liste], distfn)
        if Poids_Chemin < Poids_Trajectoire_Mini:
            Poids_Trajectoire_Mini = Poids_Chemin
            Chemin_Mini = [Premier_Sommet] + [Sommets_Suivants[k] for k in Liste]
    return Chemin_Mini, Poids_Trajectoire_Mini


g9 = [City(1, x2, "city_%d" % c) \
      for c, (x1, x2) in enumerate([[0, 0], [100, 100], [0, 100], [100, 0], [50, 50], [75, 15], [75, 35], [20, 40], [50, 20]])]


def chrono_tsp1(Sommets):
    import time
    print('-> start chrono tsp, nb sommets={0}'.format(len(Sommets)))
    t1 = time.clock()
    chemin, distance = tsp1(Sommets)
    t2 = time.clock()
    print('<- end chrono tsp, nb sommets={0}, time={1}'.format(len(Sommets), (t2-t1)))
    return (t2-t1), chemin, distance



if __name__ == '__main__':
    print(g9)
    chemin, distance = tsp1(g9, distfn=euclide)
    print(' - > '.join('[{1},{2}]'.format(c.nom, c.x1, c.x2) for c in chemin) + ' -> ... ')
    #print(' -> ...')
    print('* distance={0}'.format(distance))
