import matplotlib.pyplot as plt

def print_graphe(Sommets, Chemin_Mini, taille=100):

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


def plot_chemin(Sommets, chemin_mini, largeur, hauteur, **kwargs):
    n_points = len(Sommets)
    from matplotlib import cm
    color_palette = cm.get_cmap('jet', n_points)
    colors = color_palette(range(n_points + 1))

    def plot_arrow(s1, s2, color, f=.5):
        x0, y0 = s1.x1, s1.x2
        x1, y1 = s2.x1, s2.x2
        plt.plot([x0, x1], [y0, y1], color=color)

        f = max(f, .0001)
        dx = f * (x1 - x0)
        dy = f * (y1 - y0)
        plt.arrow(x0, y0, dx, dy,
                      color=color, head_width=3, head_length=6)

    plt.figure()
    marge = 10
    plt.axis([-marge, largeur + marge, -marge, hauteur + marge])

    plt.scatter([s[0] for s in Sommets], [s[1] for s in Sommets], s=70, color="red", marker="s", alpha=0.7)
    nb_sommets = len(chemin_mini)
    for k in range(nb_sommets-1):
        plot_arrow(chemin_mini[k], chemin_mini[k + 1], color=colors[k])
    plot_arrow(chemin_mini[-1], chemin_mini[0], color=colors[n_points])

    plt.show()


def plot_chemin2(chemin):
    n_points = len(chemin)
    from matplotlib import cm
    color_palette = cm.get_cmap('jet', n_points)
    colors = color_palette(range(n_points+1))

    # les points
    plt.scatter([chemin[i][0] for i in range(n_points)],
                [chemin[i][1] for i in range(n_points)], s=4, c='black',alpha=0.3)

    # les arcs
    [plt.plot([chemin[i][0], chemin[i+1][0]], [chemin[i][1], chemin[i+1][1]], c=colors[i]) for i in range(n_points-1)]

    plt.plot([chemin[n_points-1][0], chemin[0][0]],[chemin[n_points-1][1], chemin[0][1]], c=colors[n_points])
    plt.show()
