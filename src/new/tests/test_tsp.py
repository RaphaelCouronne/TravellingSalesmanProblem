
Graphe = [[0, 0], [100, 100], [0, 100], [100, 0], [50, 50], [75, 15], [75, 35], [20, 40], [50, 20]]

from tsp import *

chemin, distance = tsp1(Graphe)
print("* distance min={0:.2f}, chemin={1}".format(distance, chemin))
# for k in range(len(Graphe)-1) :
#    tsp1(Graphe[:k+2]) # tests OK
#print_graphe(Graphe, chemin)


#tsp1(sommets_graphe_aleatoire(9)) # tests OK

plot_times(10)
