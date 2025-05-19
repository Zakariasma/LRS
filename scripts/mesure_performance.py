import time
import functools

recursive_calls = 0


def reset_counter():
    global recursive_calls
    recursive_calls = 0


def increment_counter():
    global recursive_calls
    recursive_calls += 1


def get_counter():
    global recursive_calls
    return recursive_calls


def mesure_performance(func):
    """
    Décorateur qui mesure le temps d'exécution d'une fonction.
    Le comptage des appels récursifs doit être fait à l'intérieur de la fonction.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_counter()

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        calls = get_counter()

        execution_time = end_time - start_time
        print(f"Fonction: {func.__name__}")
        print(f"Temps d'exécution: {execution_time:.6f} secondes")
        print(f"Nombre d'appels récursifs: {calls}")

        return result, execution_time, calls

    return wrapper