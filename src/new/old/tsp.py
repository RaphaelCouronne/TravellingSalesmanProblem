from sommets import *
from naive.permutations import *
import time

def tsp1(Sommets):
    """ implémente l'algorithme de recherche de la trajectoire minimale en comparant tous les chemins """
    nb_sommets = len(Sommets)
    # on calcule une distance initiale
    Premier_Sommet, Sommets_Suivants = Sommets[0], Sommets[1:]
    Poids_Trajectoire_Mini = Poids_Trajectoire(Sommets)
    Chemin_Mini = Sommets

    for Liste in Liste_Permutees(nb_sommets):
        Poids_Chemin = Poids_Trajectoire([Premier_Sommet] + [Sommets_Suivants[k] for k in Liste])
        if Poids_Chemin < Poids_Trajectoire_Mini:
            Poids_Trajectoire_Mini = Poids_Chemin
            Chemin_Mini = [Premier_Sommet] + [Sommets_Suivants[k] for k in Liste]
    return Chemin_Mini, Poids_Trajectoire_Mini


def chrono_tsp1(Sommets):
    print('-> start chrono tsp, nb sommets={0}'.format(len(Sommets)))
    t1 = time.clock()
    chemin, distance = tsp1(Sommets)
    t2 = time.clock()
    print('<- end chrono tsp, nb sommets={0}, time={1}'.format(len(Sommets), (t2-t1)))
    return (t2-t1), chemin, distance


def print_graphe(Sommets, Chemin_Mini, taille=100):
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

    plt.figure()
    marge = 10
    plt.axis([-marge, taille+marge, -marge, taille+marge])

    plt.scatter([s[0] for s in Sommets], [s[1] for s in Sommets], s=100, color="red", marker="s")
    nb_sommets = len(Chemin_Mini)
    for k in range(nb_sommets-1):
        plot_arrow(Chemin_Mini[k], Chemin_Mini[k+1], color='blue')
    plot_arrow(Chemin_Mini[-1], Chemin_Mini[0], color='blue')

    plt.show()


def plot_times(p):
    import matplotlib.pyplot as plt
    """ trace la suite des temps de calcul """
    plt.figure()
    # nb de points
    X = [k + 2 for k in range(p)]
    Y = [chrono_tsp1(sommets_graphe_aleatoire(k))[0] for k in X]
    Z = list(map(math.log, Y))  # échelle logarithmique en ordonnées
    plt.plot(X, Z, color="red", marker="o", linestyle="-")
    plt.show()