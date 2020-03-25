from docplex.mp.model import Model


def cherche_plus_petit_cycle(all_cities, arc_vars, solution):
    # les arcs
    arcs = list(arc_vars.keys())
    # convertir la solution en un dict arcs-> 1, 0
    liens = solution.get_value_dict(arc_vars)
    # un dict des successeurs: pi -> pj
    succs = {c1: c2 for (c1, c2) in arcs if liens.get((c1, c2), 0) >= 0.5}
    nb_cities = len(all_cities)
    assert nb_cities == len(succs)

    # ensemble des points visites
    visited = set()
    plus_petit_cycle = all_cities
    for c in all_cities:
        # si on est deja passe par c on passe au suivant
        if c in visited:
            continue

        # on calcule le chemin passant par c
        cur_chemin = []
        cur_node = c
        start_node = c
        # on s arrete si on retrouve le depart sauf si on est au depart.
        while cur_node != start_node or not cur_chemin:
            # ajoute aux visites
            visited.add(cur_node)
            # on ajoute au chemin courant
            cur_chemin.append(cur_node)
            # on passe au suivant
            cur_node = succs[cur_node]

        # on a un chemin, on teste sa longueur
        if len(cur_chemin) < len(plus_petit_cycle):
            # c est un cycle, on le memorise pour tester le plus petit
            plus_petit_cycle = cur_chemin
        else:
            return cur_chemin

    # on retourne le plus court...
    return plus_petit_cycle


def coupe_cycle(cities, cycle, arc_vars, m):
    # on separe les points en deux regions: le cycle et son complementaires
    # on force au moins un arc entre les deux regions
    # 1. calculer le complementaire
    substour_set = set(cycle)
    subtour_comp = set(cprime for cprime in cities if cprime not in substour_set)
    # verification....
    assert len(substour_set) + len(subtour_comp) == len(cities)
    # ne rien faire si jamais le complementaire est vide sinon
    # posterait une contrainte impossible du type 0 >= 1 ce qui bloquerait le modele....
    if len(subtour_comp) > 0:
        # calculer l esemble des arcs possibles de C1 vers C2
        break_edges = [(c1, c2) for c1 in substour_set for c2 in subtour_comp]
        # ajouter la contrainte que cette somme vaut au moins 1 (elle peut valoir plus...)
        m.add(m.sum_vars(arc_vars[bke] for bke in break_edges) >= 1)


def tsp_lineaire(cities, distance_fn, verbose=True, iter_max=100):
    def cycle_2_string(cyc):
        return " -> ".join(c[2] for c in cyc) + " -> ..."

    # une fonction qui cree des noms: son argument est le tuple (p,q) qu il faut destructurer
    # Le nom de la variable d arc entre (0,0, "Paris") et (1,1,, "London") sera  "Paris_to_London"
    def nom_arc(pq):
        p, q = pq
        return "{0}_to_{1}".format(p[2], q[2])

    tspm = Model(name="tsp")
    nb_cities = len(cities)
    arcs = [(cities[i], cities[j]) for i in range(nb_cities) for j in range(nb_cities) if i != j]
    arc_vars = tspm.binary_var_dict(arcs, name=nom_arc)

    # les d arcs entrant et sortant
    for c in cities:
        entrants = [arc_vars[c1, c] for c1 in cities if c1 != c]
        tspm.add(tspm.sum(entrants) == 1)
        sortants = [arc_vars[c, c2] for c2 in cities if c2 != c]
        tspm.add_constraint(tspm.sum(sortants) == 1)

    # une contrainte pour supprimer les 2-cycles
    for (pi, pj) in arcs:
        if pi < pj:
            tspm.add(arc_vars[pi, pj] + arc_vars[pj, pi] <= 1)

    # objectif
    # for each arc, count the distance, and compute the sum using Model.sum(), not Python sum()
    # attention: transformer la distance (c1, c2) -> d en distance( 2-tuple) -> d

    tspm.minimize(tspm.dotf(arc_vars, lambda pq: distance_fn(pq[0], pq[1])))

    tspm.print_information()

    n_iter = 0
    while n_iter <= iter_max:
        n_iter += 1
        if verbose:
            print("-- tsp: iteration #{0}".format(n_iter))
        s = tspm.solve()
        assert s
        ch = cherche_plus_petit_cycle(cities, arc_vars, s)
        print("trouve cycle longueur: {0}: {1}".format(len(ch), cycle_2_string(ch)))
        if len(ch) == nb_cities:
            # on a fini
            lmin = s.objective_value
            return lmin, ch
        else:
            # couper le cycle
            coupe_cycle(cities, ch, arc_vars, tspm)
    #
    print("!!! nombre maximum d iterations atteint...")
    return [], -1
