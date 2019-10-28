from random import randint


def random_permut(n):
    """ renvoie une liste [sigma(1),...sigma(n-1)] avec sigma aléatoire
        retourne des indices de 1 a n
    """
    all_indices = [k for k in range(n)]
    rand_perm = []

    for i in range(n):
        # from 0 to n-2 included
        roll = randint(0, n - 1 - i)
        idx = all_indices[roll]
        rand_perm.append(idx)
        all_indices.remove(idx)  # on gère une file d'attente !

    return rand_perm


def chemin_aleatoire(liste_sommets):
    """ renvoie une trajectoire - cycle hamiltonien - aléatoire"""
    n = len(liste_sommets)
    return [liste_sommets[0]] + [liste_sommets[k + 1] for k in random_permut(n - 1)]


def win_or_lose(win_proba=0.5):
    """ Variable aleatoire a deux valeurs: True /False

    win_proba: probabilite de gain, default 1/2
    """
    bigm = 1000000
    # on genere un entier entre 0 et 1 000 000
    coin = randint(0, bigm)
    # on gagne si l entier est <= 1 000 000 * proba
    return coin <= win_proba * bigm
