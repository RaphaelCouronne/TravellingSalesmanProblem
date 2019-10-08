

def plot_chemin(chemin):
    n_points = len(chemin)
    from matplotlib import cm
    import matplotlib.pyplot as plt
    color_palette = cm.get_cmap('jet', n_points)
    colors = color_palette(range(n_points+1))
    plt.scatter([test1[i][0] for i in range(n_points)],
                [test1[i][1] for i in range(n_points)], s=4, c='black',alpha=0.3)
    [plt.plot([chemin[i][0], chemin[i+1][0]], [chemin[i][1], chemin[i+1][1]], c=colors[i]) for i in range(n_points-1)]
    plt.plot([chemin[n_points-1][0], chemin[0][0]],[chemin[n_points-1][1], chemin[0][1]], c=colors[n_points])
    plt.show()


#%% Data

from random import *

n_points = 25
test1 = [[randint(0,100), randint(0,100)] for i in range(n_points)]

import matplotlib.pyplot as plt
plt.scatter([test1[i][0] for i in range(n_points)],
            [test1[i][1] for i in range(n_points)])
plt.show()


#%%

from old.lara_code import test_gen

n_iterations = 200
n_samples = 250

meilleur_individu, min_energie = test_gen(test1, n_iterations, n_samples)
chemin_genetic = [test1[idx] for idx in meilleur_individu]+[test1[-1]]
print([test1[idx] for idx in meilleur_individu])


plot_chemin(chemin_genetic)

#%%

#chemin_g10a, distance_g10a = tsp1(test1)
#print(distance_g10a)
#print(chemin_g10a)
#plot_chemin(chemin_g10a)


