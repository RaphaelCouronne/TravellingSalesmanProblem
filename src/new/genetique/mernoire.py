Prague    = [0, 1279, 1304, 1e+20, 1e+20, 1e+20, 1e+20, 1e+20] #on ne peut pas aller dans les dernieres villes
Varna     = [1279, 0, 1e+20, 160, 438, 372, 349, 332]
Burgas    = [1304, 1e+20, 0, 290, 502, 436, 414, 393]
Constanza = [0, 158, 288, 0, 283, 217, 194, 178]
Izmail    = [0, 435, 503, 283, 0, 66, 89, 111]
Reni      = [0, 369, 437, 217, 66, 0, 23.3, 44.4]
Galati    = [0, 346, 414, 194, 89, 23.3, 0, 21.5]
Braila    = [0, 330, 392, 177, 110, 44.6, 21.7, 0]


villes_mer_noire = ["prague", "varna", "burgas", "constanza", "izmail", "reni", "galata", "braila"]
tableau_mer_noire = [Prague, Varna, Burgas, Constanza, Izmail, Reni, Galati, Braila]

matrice_mer_noire = {}
for i, v1 in enumerate(villes_mer_noire):
    for j, v2 in enumerate(villes_mer_noire):
        if i != j:
            d = tableau_mer_noire[i][j]
            if d > 0:
                #print('stop at {0}, {1}'.format(i, j))
                matrice_mer_noire[v1, v2] = tableau_mer_noire[i][j]



from genetique.alg_gen2 import Dynamique_Population
from common.distances import *

c = Dynamique_Population(villes_mer_noire, 30, 20, distfn=matrice_vers_fonction(matrice_mer_noire), )
print(c)