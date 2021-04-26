


import random
import math
import timeit


def generate_vector(n):
    x = [random.uniform(-5.12, 5.12) for i in range(n)]

    return x

def rastrigin_func(x):
    n = len(x)

    func_value = 10 * n

    for value in x:
        func_value = func_value + value ** 2 - 10 * math.cos(2 * math.pi * value)

    return func_value


def get_dimenssion():
    print("Algoritm euristic pt. functia lui Rastrigin:")
    print("Introduceti dimensiunea n a functiei: ")

    n = int(input())

    return n


def det_min():
    n = get_dimenssion()
    min_value = 1000000

    for _i in range(1000001):
        x = generate_vector(n)
        rastrigin = rastrigin_func(x)
        min_value = min(min_value, rastrigin)

    return min_value



print(timeit.timeit(det_min, number=1))
