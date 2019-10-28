import math

# les points sont des tuples de deux coordonnees (flottants), soit x,y
# soit longitude, latitude
# une distance est une fonction qui prend deux tuples et retourne un flottant

from collections import namedtuple

# le type Ville est un tuple nomme atrois champs:
#  -- son nom ("Paris", "Lyon", ..)
#  -- deux coordonnees x1, et x2 peut etre
City = namedtuple("City", ["x1", "x2", "nom"])

def genere_liste_sommets(liste_x1x2s):
    return [City(x1, x2, "c%d" % c) for c,(x1, x2) in enumerate(liste_x1x2s)]

def euclide(c1, c2):
    x11, x12,_ = c1
    x21, x22, _ = c2
    return math.sqrt( (x21 -x11)**2 + (x12-x22)**2)

def manhattan(c1, c2):
    x11, x12, _ = c1
    x21, x22, _ = c2
    return abs(x11-x21) + abs(x21-x22)

def haversine2(a):
    # square of sinus of half angle
    sin_half = math.sin(a / 2)
    return sin_half * sin_half

DEG2RAD = math.pi / 180.

def earth_distance(c1, c2, rayon=6373):
    """" retourne le distance spherique entre deux villes (City)

    :param c1: une ville (City)
    :param c2: a (longitude, latitude) 2-tuple in radians
    :param rayon: le rayon de la terre en km (changer par miles si besoin
    :return:
    """
    lon1, lat1, _ = c1
    lon2, lat2, _ = c2
    # tconversion degres radians
    rlon1, rlat1 = DEG2RAD * lon1, DEG2RAD* lat1
    rlon2, rlat2 = DEG2RAD * lon2, DEG2RAD* lat2
    assert 0 <= lat1 < 1.6  # less than pi/2
    assert 0 <= lat2 < 1.6

    dlon = rlon2 - rlon1
    dlat = rlat2 - rlat1
    a = haversine2(dlat) + math.cos(rlat1) * math.cos(rlat2) * haversine2(dlon)
    c = 2 * math.asin(math.sqrt(a))
    d = rayon * c  # in kms
    return math.ceil(d)

def distance_chemin(sommets, distfn=euclide):
    """ calcule le poids affecté à une chaîne de sommets """
    nb_sommets = len(sommets)
    d = sum( distfn(sommets[k], sommets[k + 1]) for k in range(0, nb_sommets-1))
    return d + distfn(sommets[-1], sommets[0])  # pour boucler le cycle

def distance2matrix(villes, distfn):
    """ Calcule une matrice de distance a partir d un eliste de villes et d une fonction.

    :param villes: liste de villes de taille N
    :param distfn: une fonction (Ville,Ville) -> float qui retourne la distance entre deux villes


    :return: une matrice[NxN] avec les distances
    """
    dist_m = {}
    for v1 in villes:
        for v2 in villes:
            d = 0 if v1 == v2 else distfn(v1, v2)
            dist_m[v1, v2] = d
    return dist_m


def matrice_vers_fonction(distm, default_dist=1e+20):
    """ Convertit une matrice de distance enune fonction.

    :param distm: la matrice de distance
    :param default_dist: la distance retournee quand le couple ne figure pas dansla matrice,
        par defaut tres grande (1e+20 = 1 avec 20 zeros derriere)

    Quand les deux sites sont les memes, retourne 0

    :return: une fonction qui prend un couple de sommets et retourne une distance.
    """
    # si le couple (s1, s2) n est pas dan sla matrice, on considere la distance comme infinie
    def distance_fn(s1, s2):
        if s1 == s2: # retourne 0 si s1 == s2
            return 0
        else:
            # si le tuple(s1, s2) n est pas une cle, la distance est infinie
            return distm.get((s1, s2), default_dist)
    return distance_fn