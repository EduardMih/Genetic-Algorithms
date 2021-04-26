


import math
import numpy
from random import choice
from random import random

local_max = {}

def poli(x):
    value = x ** 3 - 60 * x ** 2 + 900 * x + 100

    return value


def decode(bitstring):
    value = 0

    for i in range(5):
        value = value * 2
        value = value + bitstring[i]

    return value




def create_neigh(bitstring, pos):
    new_neigh = bitstring.copy()
    
    if new_neigh[pos] == 0:
        new_neigh[pos] = 1

    else:

        new_neigh[pos] = 0
    
    return new_neigh


def first_improve(bitstring, fct):
    indexes = list(range(5))
    current_value = fct(decode(bitstring))

    while indexes:
        index = choice(indexes)
        candidate = create_neigh(bitstring, index)
        indexes.remove(index)

        if fct(decode(candidate)) > current_value:

            return candidate
    
    return bitstring


def best_improve(bitstring, fct):
    best = bitstring.copy()

    for i in range(5):
        candidate = create_neigh(bitstring, i)
        if fct(decode(candidate)) > fct(decode(best)):
            best = candidate

    return best


def hill_climbing(fct, improve_meth):
    t = 0
    best = [choice([0, 1]) for _ in range(5)]
    while  t <= 100:
        isLocal = False
        candidate = [choice([0, 1]) for _ in range(5)]
        cc = candidate.copy()

        while isLocal == False:
            neighbour = improve_meth(candidate, fct)
            if fct(decode(neighbour)) > fct(decode(candidate)):
                candidate = neighbour
            
            else:

                isLocal = True
        
        if decode(candidate) in local_max:
            local_max[decode(candidate)].append(decode(cc))

        else:

            local_max[decode(candidate)] = [decode(cc)]
        
        t = t + 1

        if fct(decode(candidate)) > fct(decode(best)):
            best = candidate
    
    return best


def FIHC():
    for _ in range(30):
        hill_climbing(poli, first_improve)
    
    print("Pentru First:")

    for item in local_max:
        print(item, "->", set(local_max[item]))


def BIHC():
    for _ in range(30):
        hill_climbing(poli, best_improve)

    print("Pentru Best:")

    for item in local_max:
        print(item, "->", set(local_max[item]))


FIHC()
local_max = {}
BIHC()
