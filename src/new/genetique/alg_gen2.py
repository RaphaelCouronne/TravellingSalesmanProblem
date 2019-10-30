from common.aleatoire import *
from common.distances import *

from random import randint


### Génération d'une population aléatoire ###

def individu_alea(Liste_Sommets):
    return chemin_aleatoire(Liste_Sommets)


def Generation_Pop_Alea(Liste_Sommets, pop_size, distfn=None):
    """ génère p individus aléatoirement """
    return [individu_alea(Liste_Sommets) for _ in range(pop_size)]


def Individu_Plus_Courts_Trajets(Liste_Sommets, i, distfn):
    """ détermine à partir du sommet i un cycle hamiltonien
        en cherchant les sommets plus proches
    """
    Sommets = Liste_Sommets.copy()
    initiale = Sommets[i]
    Liste_Temp = [initiale]
    Sommets.remove(initiale)  # on gère une file d'attente

    while Sommets:
        Distance_Mini, Ville_Mini = distfn(Sommets[0], Liste_Temp[-1]), Sommets[0]
        for ville in Sommets[1:]:
            distance_temp = distfn(ville, Liste_Temp[-1])
            if distance_temp < Distance_Mini:
                Distance_Mini, Ville_Mini = distance_temp, ville
        Liste_Temp.append(Ville_Mini)
        Sommets.remove(Ville_Mini)
    # il faut maintenant effectuer le cycle sur Liste_Temp pour commencer à Sommets[0]
    depart = Liste_Sommets[0]
    trouve = -1
    for k in range(len(Liste_Temp)):
        if Liste_Temp[k] == depart:
            trouve = k
            break
    assert trouve >= 0
    return Liste_Temp[trouve:] + Liste_Temp[:trouve]


def Generation_Pop_Semi_Alea(Liste_Sommets, p, distfn):
    """ génère une population semi-aléatoire """
    halfp = p // 2
    return Generation_Pop_Alea(Liste_Sommets, halfp) \
           + [Individu_Plus_Courts_Trajets(Liste_Sommets, randint(0, len(Liste_Sommets) - 1), distfn) for _ in
              range(halfp)]


# --
# Algorithme genetique
#
# 1. definition de la fonction d adaptation.
#
# L adaptation d un individu est ici la distance totale d un chemin
# l individu ayant le plus court chemin est le plus adapte.
#
# ---

def adaptation_individu(individu, distfn):
    """ calcule la fonction d'adaptation correspondant  à un individu <-> cycle hamiltonien

    Utilise la fonction de distance

    retourne un nombre flottant
     """
    n = len(individu)
    adapt = sum(distfn(individu[k], individu[k + 1]) for k in range(n - 1))
    adapt += distfn(individu[-1], individu[0])  # pour boucler le cycle
    return adapt


# ---
# Hybdidation de deux individus
#
# a partir de deux chemins (differents?)
# on en genere deux nouveaux de la facon suivante:
# pour le chemin C1,
# on garde le chemin inchange jusqu a i-1
# et complete par les points de C2 qui ne sont pas deja dans C1, dan sl ordre de C2.
# Exemple:
# C1 = [1, 2, 3, 4]
# C2 = [3, 2, 4, 1]
# on suppose i = 2
# C'1 = [1] + [3, 2, 4] = [1,3,2,4]
# C'2 = [3] + [1, 2, 4] = [3,1,2,4]

def Hybridation(Individu1, Individu2, i):
    """ renvoie à partir de deux individus <-> cycles hamiltoniens
    deux autres individus après un cross-over des chromosomes
    à l'allèle (index) i avec i compris entre 1 et n-2

    Cette hybdridation est parfaitement deterministe,
    sans aucun caractere aleatoire.
    """
    n = len(Individu1)
    assert len(Individu2) == n
    assert i >= 1
    assert i <= n - 2
    # Liste1, Liste2 = Individu1.copy(), Individu2.copy()

    list1 = Individu1[:i]
    list2 = Individu2[:i]
    mix1 = Individu1[:i]
    for x in Individu2:
        if x not in list1:
            mix1.append(x)
    mix2 = list2
    for z in Individu1:
        if z not in list2:
            mix2.append(z)

    assert len(mix1) == n
    assert len(mix2) == n
    return [mix1, mix2]


def Hybridation_Alea(Individu1, Individu2):
    """
    Variante aleatoire de l'hybridation, on tire au sort l allele.
    :param Individu1:
    :param Individu2:

    :return:
    """
    n = len(Individu1)
    i = randint(2, n - 2)  # i=1 ou i=n n'engendre pas d'hybridation effective
    return Hybridation(Individu1, Individu2, i)


def Mutation(Individu, k, l):
    """
    mute l'individu en modifiant les indices k,k+1,...,l-1,l
    en l,l-1,...,k+1,k en partant de 1 <= k < l< n

    Retourne: un chemin resultant de la mutation.

    """
    assert k <= l - 1
    assert l < len(Individu)

    if l - 1 == k:
        # inchange jusqu a (k-1) puis (k+1,k) puis inchange de k+2 a N
        return Individu[:k] + [Individu[k + 1], Individu[k]] + Individu[k + 2:]
    elif l - 2 == k:
        return Individu[:k] + [Individu[k + 2], Individu[k + 1], Individu[k]] + Individu[k + 3:]
    else:
        return Individu[:k] + [Individu[l], Individu[l - 1]] + Individu[k + 2:l - 1] + \
               [Individu[k + 1], Individu[k]] + Individu[l + 1:]


def Mutation_Alea(Individu):
    """ modélise une mutation aléatoire

    on tire au sort k dans {1..n-2} n-2 exclus
    on tire au sort l dans k+1, n-1 , n-1 exclus

    """
    n = len(Individu)
    k = randint(1, n - 2)
    l = randint(k + 1, n - 1)
    return Mutation(Individu, k, l)


def Echange2(Individu, k, l):
    """ mute l'individu en moechangeant les alleles k et l (k < l)

    Note: retourne une copie modifiee de individu.
    """
    assert k <= l - 1
    assert l < len(Individu)
    IndividuEchange = Individu.copy()
    IndividuEchange[k] = Individu[l]
    IndividuEchange[l] = Individu[k]
    return IndividuEchange


def echange2_alea(Individu):
    """ Effectue l echange de deux alleles tirees au sort K < l

    :param Individu:
    :return:
    """
    n = len(Individu)
    k = randint(1, n - 2)
    l = randint(k + 1, n - 1)
    return Echange2(Individu, k, l)


### Sélection des individus ###


def Selection_Tournoi(Individu1, Individu2, distfn, win_proba=0.85):
    """ renvoie le vainqueur entre deux individus,
       en attribuant 85% de chance de viectoire pour le mieux adapté

    TODO: pourquoi copier ici??
       """
    if adaptation_individu(Individu1, distfn) < adaptation_individu(Individu2, distfn):  # individu 1 mieux adapté que 2
        Match = [Individu1.copy(), Individu2.copy()]
    else:
        Match = [Individu2.copy(), Individu1.copy()]

    if win_or_lose(win_proba=win_proba):
        return Match[0]
    else:
        # danavec une probabilite 1 - win_proba (15%) le moins adapte gagne!
        return Match[1]


def Deux_Adversaires_Alea(Population):
    """ renvoie un match entre deux adversaires d'une population """
    q = len(Population)
    k = l = 0
    while k == l:
        # Liste_Indices = list(range(q))
        k, l = randint(0, q - 1), randint(0, q - 1)
    # k = numéro du premier candidat
    # ## en théorie randint(0,q-1) et randint(0,q-2)...
    # Liste_Indices.remove(k)  # pour ne pas choisir le même candidat
    # m = Liste_Indices[l]  # numéro du second candidat
    return Population[k], Population[l]


### Choix de la meilleur moitié d'une population et choix du meilleur 

def meilleure_moitie(Population, distfn):
    """ Retourne la moitie la mieux adaptee d une population.
    """
    pop_triee = Population.copy()
    # on trie la population par adaptation croissante, avec list.sort()
    pop_triee.sort(key=lambda x: adaptation_individu(x, distfn))
    # on garde les q//2 meilleurs
    q = len(Population)
    return pop_triee[:q // 2]


def Meilleur_Individu(Population, distfn):
    " renvoie l'individu le mieux adapté dans une population """
    meilleur_chemin = None
    meilleure_adaptation = 1e+20
    for x in Population:
        adapt = adaptation_individu(x, distfn)
        if adapt < meilleure_adaptation:
            meilleur_chemin = x
            meilleure_adaptation = adapt

    return meilleur_chemin, meilleure_adaptation


### Construction de la génération suivante ###

def calcule_generation_suivante(Population, distfn):
    """ calculela population à la génération suivante """
    q = len(Population)
    Population_Temp = []

    # stats
    nombre_mutations = 0
    nombre_echanges = 0
    nombre_hybridations = 0

    proba_gagnant = 0.85  # la probabilite de choisir le gagnat dans les tournois
    proba_hybridation = 0.20  # la probabilite de faire une hybdridation
    proba_mutation = 0.10
    proba_echange = 0.03

    # extraction population temporaire: attention il peut y avoir des doublons...
    # population temp= les gagnants
    for k in range(q):
        Advers = Deux_Adversaires_Alea(Population)
        Population_Temp.append(Selection_Tournoi(Advers[0], Advers[1], distfn, win_proba=proba_gagnant))
    # Population_Temp = population des gagnants des matchs

    ## modélisation des hybridations sur cette Population_Temp
    # proba qu'une hypridation ait lieu entre deux chromosomes: 1/5


    for k in range(q - 1):
        for l in range(q - 1 - k):
            if win_or_lose(proba_hybridation):
                #print('-- hybridation k={0}, l={1}'.format(k, k+l+1))
                nombre_hybridations += 1
                Individus_Hybr = Hybridation_Alea(Population_Temp[k], Population_Temp[k + l + 1])
                Population_Temp[k], Population_Temp[k + l + 1] = Individus_Hybr[0], Individus_Hybr[1]

    ## modélisation des mutations
    for i in range(len(Population_Temp)):
        Individu_at_i = Population_Temp[i]
        if win_or_lose(proba_mutation):  # une mutation a lieu !!
            nombre_mutations += 1
            #print('-- mutation #{}'.format(nombre_mutations))
            # il FAUT modifier le tableau
            resultat_mutation = Mutation_Alea(Individu_at_i)
            Population_Temp[i] = resultat_mutation

    for i in range(len(Population_Temp)):
        Individu_at_i = Population_Temp[i]
        if win_or_lose(win_proba=proba_echange):
            nombre_echanges += 1
            #print('-- echange #{}'.format(nombre_mutations))
            Population_Temp[i] = echange2_alea(Individu_at_i)

    print("-- #hybridations={0}, mutations={1}, #echanges={2}".format(nombre_hybridations, nombre_mutations, nombre_echanges))

    ## choix des meilleurs individus de Population (génération g)
    # (on en prend p//2)
    # et des meilleurs individus de Population_Temp (génération g+1)(on en prend p//2)
    return meilleure_moitie(Population, distfn) + meilleure_moitie(Population_Temp, distfn)


# noinspection PyUnusedLocal
def no_animation(k, pop, chemin, adaptation):
    pass


def print_score(k, pop, chemin, adaptation):
    print("- population #{0} adaptation: {1}".format(k, adaptation))


def Dynamique_Population(Liste_Sommets, nb_gens, taille_pop=30,
                         distfn=euclide,
                         nb_bloque_max=30,
                         gen_animation_fn=print_score):
    """ Lance l'algorithme sur nb_gens generations

    :param Liste_Sommets: une liste de villes (City)
    :param nb_gens: nombre de generations >= 2
    :param taille_pop: la taille des populations (defaut 30)
    :param distfn: la fonction de distance
    :param gen_animation_fn:une fonction appelee a chaque generation avec la
        population et le numero de la generation

    :return: le meilleur chemin trouve
    """
    ## Choixi du type de population initiale
    # Population = Generation_Pop_Alea(Liste_Sommets, taille_pop, distfn)  # population de départ totalement aléatoire
    Population = Generation_Pop_Semi_Alea(Liste_Sommets, taille_pop, distfn)  # population de départ semi-aléatoire
    ##

    chemin, adaptation = Meilleur_Individu(Population, distfn)
    gen_animation_fn(0, Population, chemin, adaptation)
    bloque = 0
    for k in range(1, nb_gens + 1):
        print("-- iteration {0}".format(k))
        Population = calcule_generation_suivante(Population, distfn)

        prec_adaptation = adaptation
        chemin, adaptation = Meilleur_Individu(Population, distfn)
        gen_animation_fn(k, Population, chemin, adaptation)
        if adaptation >= prec_adaptation - 1e-6:
            print("*** stationnaire a l iteration {0}, nb bloques = {1}".format(k, bloque))
            bloque += 1
            if bloque >= nb_bloque_max:
                break
        else:
            bloque = 0

    chemin, adaptation = Meilleur_Individu(Population, distfn)

    return chemin
