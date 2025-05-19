import time
from mesure_performance import increment_counter


def trouveVoisinCommunDe(ensemble, sommet, graphe):
    return set(v for v in ensemble if v in graphe[sommet])


def choisirPivot(P, X, graphe):
    union = P.union(X)
    pivot = max(union, key=lambda u: len(graphe[u].intersection(P)), default=None)
    return pivot


def BronKerboschPivot(P, R, X, graphe, recursif):

    if recursif:
        increment_counter()

    cliques_maximales = []

    if len(P) == 0 and len(X) == 0:
        return [R.copy()]

    u = choisirPivot(P, X, graphe)
    voisins_u = graphe[u] if u is not None else set()
    P_sans_voisins_u = P.difference(voisins_u)

    for v in list(P_sans_voisins_u):
        R_rec = R.union({v})
        P_rec = trouveVoisinCommunDe(P, v, graphe)
        X_rec = trouveVoisinCommunDe(X, v, graphe)

        nouvelles_cliques = BronKerboschPivot(P_rec, R_rec, X_rec, graphe, True)
        cliques_maximales.extend(nouvelles_cliques)

        P.remove(v)
        X.add(v)

    return cliques_maximales


if __name__ == "__main__":
    G = {
        1: {2, 3},
        2: {1, 3, 5},
        3: {1, 2, 4},
        4: {3, 5},
        5: {2, 4}
    }

    P = set(G.keys())
    R = set()
    X = set()

    start_time = time.time()
    cliques = BronKerboschPivot(P, R, X, G)
    end_time = time.time()

    print("Cliques maximales trouvées (avec pivot):")
    for clique in cliques:
        print(clique)

    print(f"Temps d'exécution: {end_time - start_time} secondes")