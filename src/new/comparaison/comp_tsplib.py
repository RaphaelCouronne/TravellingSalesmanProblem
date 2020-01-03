import os

from os.path import dirname as dn
from common.distances import City, euclide, earth_distance

from genetique.alg_gen2 import Dynamique_Population

def distance_par_nom(dn):
    if 'GEO' in dn:
        return earth_distance
    else:
        return euclide

def read_tsp_file(basename):
    tsp_path = os.path.join(dn(dn(__file__)), "tsplib", basename + ".tsp")
    with open(tsp_path, "r") as tspf:
        lines = tspf.readlines()
        nom_distance = lines[4].strip().split(':')[1]

        g = []
        for l in lines[6:-2]:
            row = l.strip().split(' ')
            n = row[0]
            x1 = float(row[1])
            x2  = float(row[2])
            g.append(City(x1, x2, n))
        return  g, distance_par_nom(nom_distance)

def print_resultats(chemin, distance):
    print('* distance = {0}'.format(distance))
    return " -> ".join(c.nom for c in chemin) + ' ...'

tsplib_resultats = { 'att48' : 10628, 'berlin52' : 7542, 'lin105' : 14379, 'pr136' : 96772, 'ulysses22' : 7013}

def comp_tsplib(basename, verbose=True):
    g, d = read_tsp_file(basename) #liste des villes
    chemingen, distgen = Dynamique_Population(g, nb_gens=30, taille_pop=50, distfn=d, verbose=verbose)
    print(print_resultats(chemingen, distgen))
    distvraie = tsplib_resultats.get(basename)
    diff = (abs(distgen - distvraie) / distvraie)*100
    print(' ecart tsplib={0:.2f}%'.format(diff))
    return diff

comp_tsplib('berlin52')








