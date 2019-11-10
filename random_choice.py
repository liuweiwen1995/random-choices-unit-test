import random
from itertools import compress


def search_interval(l, x):
    """Return the index of the interval of item i in list l
    The first interval is (-inf, l[0]]

    """
    low, high = 0, len(l)
    if x > l[high - 1]:
        raise ValueError('x out of range.')
    while low < high:
        mid = (low + high) // 2
        if x > l[mid]:
            low = mid + 1
        else:
            high = mid
    return low


def accumulate(x):
    """Return the cumulative sum of x

    """
    it = iter(x)
    total = next(it)
    yield total
    for i in it:
        total += i
        yield total


def random_choice(population, weights=None, k=1):
    """Generate weighted items.

    If weights are not specified, return the uniform sampling results

    """
    if isinstance(population, set):
        population = list(population)
    if not isinstance(population, list) and not isinstance(population, tuple):
        raise TypeError('Population must be a sequence or a set.')

    n = len(population)
    if not isinstance(k, int):
        raise TypeError('k must be an integer.')
    elif k <= 0:
        raise ValueError('k must be a positive integer.')
    if weights is None:
        weights = [1] * n
    if len(weights) != n:
        raise ValueError('The number of weights does not match the population.')
    for x in weights:
        if x < 0:
            raise ValueError('Weights must be non-negative.')
    # remove 0s in ```population''' and ```weights'''
    population, weights = zip(*compress(zip(population, weights), weights))
    return [population[search_interval(list(accumulate(weights)), random.random() * sum(weights))] for _ in range(k)]


