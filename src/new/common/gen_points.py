from random import uniform

from common.distances import City

def sommets_graphe_alea(n, largeur, hauteur, bord=20):
    """ Retourne n sommets aleatoires dans un rectangle largeur x hauteur, non compris les bords
    :param n:
    :param largeur:
    :param hauteur:
    :param bord:
    :return:
    """
    return [City(uniform(bord, largeur - bord), uniform(bord, hauteur - bord), "city_%d" %(i+1)) for i in range(n)]


def print_as_data(ls):
    print("[")
    print(", ".join("({0:.0f}, {1:.0f})".format(v.x1, v.x2) for v in ls))
    print("]")