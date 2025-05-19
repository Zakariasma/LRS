import time
import random
import sys
from mesure_performance import mesure_performance

from BrutForceClique import brutForceClique
from BronKerbosh import BronKerbosch
from BronKerboshPivot import BronKerboschPivot
from BronKerboschDegenerescence import BronKerboschDegenerescence
import random

def generer_graphe(n, p):
    """
    P = proba de connexion
    """
    graphe = {i: set() for i in range(1, n + 1)}

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if random.random() < p:
                graphe[i].add(j)
                graphe[j].add(i)

    return graphe


def calculer_degenerescence(G):
    H = {v: set(neighbors) for v, neighbors in G.items()}
    n = len(H)

    degenerescence = 0
    ordre = []

    while H:
        # Trouver le sommet de degré minimal
        min_deg_v = min(H, key=lambda v: len(H[v]))
        min_deg = len(H[min_deg_v])
        degenerescence = max(degenerescence, min_deg)
        ordre.append(min_deg_v)

        for u in H[min_deg_v]:
            H[u].remove(min_deg_v)

        del H[min_deg_v]

    return degenerescence, ordre


@mesure_performance
def run_bruteforce(G):
    return brutForceClique(G)


@mesure_performance
def run_bronkerbosch(G):
    P = set(G.keys())
    R = set()
    X = set()
    return BronKerbosch(P, R, X, G, False)


@mesure_performance
def run_bronkerbosch_pivot(G):
    P = set(G.keys())
    R = set()
    X = set()
    return BronKerboschPivot(P, R, X, G, False)


@mesure_performance
def run_bronkerbosch_degenerescence(G):
    return BronKerboschDegenerescence(G)


def main():
    # Tailles de graphes à tester
    tailles = [10, 20, 150, 300, 500, 1000, 10000]

    # Résultats
    resultats = {}

    print("=== TEST DE PERFORMANCE DES ALGORITHMES DE RECHERCHE DE CLIQUES MAXIMALES ===\n")
    print("=== TESTS SUR DES GRAPHES CREUX ===\n")

    for n in tailles:
        print(f"\n{'-' * 60}")
        print(f"Test avec un graphe creux à {n} sommets")
        print(f"{'-' * 60}")

        # Générer le graphe creux (2/n ou 1/n ou pourcentage sous la forme 0.x)
        G = generer_graphe(n, 2/n)

        # Informations sur le graphe
        total_aretes = sum(len(voisins) for voisins in G.values()) // 2
        degenerescence, _ = calculer_degenerescence(G)
        print(f"Graphe généré: {n} sommets, {total_aretes} arêtes, dégénérescence: {degenerescence}")

        result_key = f"{n}_{total_aretes}"
        resultats[result_key] = {}
        algorithmes = []

        # BrutForceClique complexité exp donc pas possible de lancer sur nombre de sommet >100 sinon temps infini
        if n <= 101:
            algorithmes.append(("BrutForceClique", run_bruteforce))

        algorithmes.extend([
            ("BronKerbosch", run_bronkerbosch),
            ("BronKerboschPivot", run_bronkerbosch_pivot),
            ("BronKerboschDegenerescence", run_bronkerbosch_degenerescence)
        ])

        for nom, algo in algorithmes:
            print(f"\nTest de {nom}:")
            try:
                old_recursion_limit = sys.getrecursionlimit()
                sys.setrecursionlimit(10000)

                try:
                    result, time_taken, recursive_calls = algo(G)
                    nb_cliques = len(result) if result else 0
                    print(f"Nombre de cliques maximales trouvées: {nb_cliques}")

                    resultats[result_key][nom] = {
                        "temps": time_taken,
                        "appels_recursifs": recursive_calls,
                        "nb_cliques": nb_cliques
                    }

                except Exception as e:
                    print(f"Erreur lors de l'exécution de {nom}: {e}")
                    resultats[result_key][nom] = {
                        "temps": -1,
                        "appels_recursifs": -1,
                        "nb_cliques": -1
                    }

                sys.setrecursionlimit(old_recursion_limit)

            except KeyboardInterrupt:
                print("Interrompu par l'utilisateur")
                resultats[result_key][nom] = {
                    "temps": -1,
                    "appels_recursifs": -1,
                    "nb_cliques": -1
                }


if __name__ == "__main__":
    main()
