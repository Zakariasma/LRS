import time
from BronKerboshPivot import BronKerboschPivot, choisirPivot, trouveVoisinCommunDe


def calculer_ordre_degenerescence(graphe):
    # increment_counter()
    n = len(graphe)
    degre = {v: len(graphe[v]) for v in graphe}
    max_degre = max(degre.values()) if degre else 0
    buckets = [[] for _ in range(max_degre + 1)]

    for v in graphe:
        buckets[degre[v]].append(v)

    ordre_degenerescence = []

    for d in range(max_degre + 1):
        while buckets[d]:
            v = buckets[d].pop()
            ordre_degenerescence.append(v)

            for u in graphe[v]:
                if u not in ordre_degenerescence:
                    d_u = degre[u]
                    if d_u > d:
                        buckets[d_u].remove(u)
                        degre[u] -= 1
                        buckets[d_u - 1].append(u)

    return ordre_degenerescence


def construire_sous_graphe(graphe, P, X):
    H_p_x = {}
    union = P.union(X)

    for v in union:
        H_p_x[v] = set()

    for u in union:
        for v in graphe[u].intersection(union):
            if u in P or v in P:
                H_p_x[u].add(v)
                H_p_x[v].add(u)

    return H_p_x


def BronKerboschDegenerescence(graphe):
    ordre_degenerescence = calculer_ordre_degenerescence(graphe)
    cliques_max = []

    position = {v: i for i, v in enumerate(ordre_degenerescence)}

    for vi in ordre_degenerescence:
        P = {v for v in graphe[vi] if position[v] > position[vi]}
        X = {v for v in graphe[vi] if position[v] < position[vi]}

        sous_graphe = construire_sous_graphe(graphe, P, X)

        nouvelles_cliques = BronKerboschPivot(P, {vi}, X, sous_graphe, False)

        for clique in nouvelles_cliques:
            cliques_max.append(set(clique))

    return cliques_max



if __name__ == "__main__":
    G = {
        1: {2, 3},
        2: {1, 3, 5},
        3: {1, 2, 4},
        4: {3, 5},
        5: {2, 4}
    }

    # Test et analyse
    print("===== ANALYSE DES APPELS RÉCURSIFS =====")

    # Test normal
    print("\n===== RÉSULTATS DE L'ALGORITHME =====")
    start_time = time.time()
    cliques = BronKerboschDegenerescence(G)
    end_time = time.time()

    print("Cliques maximales trouvées (avec dégénérescence optimisée):")
    for clique in cliques:
        print(clique)

    print(f"Temps d'exécution: {end_time - start_time} secondes")