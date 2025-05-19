import time
from mesure_performance import increment_counter


def est_clique(graphe, sommets):
    for i in sommets:
        for j in sommets:
            if i != j and j not in graphe[i]:
                return False
    return True


def est_maximale(graphe, clique):
    for sommet in graphe:
        if sommet not in clique:
            est_connecte_a_tous = True
            for s in clique:
                if s not in graphe[sommet]:
                    est_connecte_a_tous = False
                    break
            if est_connecte_a_tous:
                return False
    return True


def brutForceClique(graphe):
    increment_counter()
    tous_sommets = list(graphe.keys())
    n = len(tous_sommets)
    cliques_maximales = []

    for i in range(1, 2 ** n):
        sous_ensemble = {tous_sommets[j] for j in range(n) if (i & (1 << j))}

        if est_clique(graphe, sous_ensemble):
            if est_maximale(graphe, sous_ensemble):
                cliques_maximales.append(sous_ensemble)

    return cliques_maximales


if __name__ == "__main__":
    G = {
        1: {2, 3},
        2: {1, 3, 5},
        3: {1, 2, 4},
        4: {3, 5},
        5: {2, 4}
    }

    start_time = time.time()
    cliques = brutForceClique(G)
    end_time = time.time()

    print("Cliques maximales trouvées (brute force):")
    for clique in cliques:
        print(clique)

    print(f"Temps d'exécution: {end_time - start_time} secondes")