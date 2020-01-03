

from common.gen_points import sommets_graphe_alea
from genetique.alg_gen2 import *

Liste_Sommets = sommets_graphe_alea(n=40, largeur=300, hauteur=200)

def print_as_data(ls):
    print("[")
    print(", ".join("({0:.0f}, {1:.0f})".format(v.x1, v.x2) for v in ls))
    print("]")

print_as_data(Liste_Sommets)
g35 = [
    (226.11, 88.86), (264.20, 86.78), (150.04, 43.06), (198.85, 160.40), (219.23, 65.55), (210.13, 146.72),
    (91.91, 84.86), (231.76, 158.05), (188.13, 52.29), (31.29, 149.04), (221.82, 62.03), (127.41, 115.26),
    (194.70, 101.15), (46.86, 53.13), (190.05, 138.86), (56.05, 97.89), (39.25, 149.82), (254.44, 39.80),
    (60.51, 99.72), (164.83, 158.71), (140.70, 28.80), (223.47, 47.76), (148.08, 49.83), (233.95, 123.97),
    (211.44, 156.21), (230.72, 131.01), (178.57, 56.23), (139.19, 59.56), (190.01, 93.80), (185.76, 121.41),
    (164.68, 167.15), (31.68, 49.51), (247.81, 90.17), (58.72, 46.49), (192.47, 28.25), (236.20, 105.11),
    (47.87, 86.72), (202.33, 62.91), (143.54, 96.76), (21.19, 101.33)]


l35 = genere_liste_sommets(g35)

chemin= Dynamique_Population(l35, nb_gens=100, taille_pop=40, nb_bloque_max=10, gen_animation_fn=print_score)

from visu.plot import *

plot_chemin(l35, chemin, largeur= 300, hauteur=200)