import time
from mesure_performance import increment_counter

def trouveVoisinCommunDe(ensemble, sommet, graphe):
    return set(v for v in ensemble if v in graphe[sommet])

def BronKerbosch(P, R, X, graphe, recursif):
    cliques_maximales = []

    if recursif:
        increment_counter()

    if len(P) == 0 and len(X) == 0:
        return [R.copy()]

    P_copy = P.copy()
    for i in P_copy:
        R_rec = R.union({i})
        P_rec = trouveVoisinCommunDe(P, i, graphe)
        X_rec = trouveVoisinCommunDe(X, i, graphe)

        nouvelles_cliques = BronKerbosch(P_rec, R_rec, X_rec, graphe, True)
        cliques_maximales.extend(nouvelles_cliques)

        P.remove(i)
        X.add(i)

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
    cliques = BronKerbosch(P, R, X, G)
    end_time = time.time()

    print("Cliques maximales trouvées:")
    for clique in cliques:
        print(clique)

    print(f"Temps d'exécution: {end_time - start_time} secondes")
