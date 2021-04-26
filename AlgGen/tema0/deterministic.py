


import math
import numpy
import timeit

x = [None] * 7
min_val=1000

def rastrigin_func(x):
    n = len(x)

    func_value = 10 * n

    for value in x:
        func_value = func_value + value ** 2 - 10 * math.cos(2 * math.pi * value)

    return func_value


def get_dimenssion():
    print("Algoritm deterministic pt. functia lui Rastrigin:")
    print("Introduceti dimensiunea n: ")

    n = int(input())

    return n


def det_min(pos, n):
    global x
    global min_val


    for val in numpy.arange(-5.12, 5.12, 0.01):
        x[pos] = val

        if pos == n:
           val = rastrigin_func(x[:n])
           min_val = min(min_val, val)
           break

        else:

            if pos < n:
                det_min(pos + 1, n) 


def run_alg():
   n = get_dimenssion()
   det_min(0, n)
   print(min_val)

print(timeit.timeit(run_alg, number=1))
