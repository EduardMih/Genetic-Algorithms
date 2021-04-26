


import math
import numpy
from random import choice
from random import random
from timeit import default_timer as timer


length = 0
dimension = 0
a = 0
b = 0
prec = 0

def DeJong(x):
    global dimension
    value = 0
    dim = dimension
    

    for i in range(dim):
        value = value + x[i] ** 2

    return value


def Schwefel(x):
    global dimension
    value = 0
    dim = dimension

    for i in range(dim):
        value = value + (-x[i]) * math.sin(math.sqrt(abs(x[i])))

    return value


def Rastrigin(x):
    global dimension
    
    dim = dimension
    value = 10 * dim

    for i in range(dim):
        value = value + (x[i] ** 2 - 10 * math.cos(2 * math.pi * x[i]))

    return value


def Michalewicz(x):
    global dimension
    dim = dimension
    value = 0
    m = 10

    for i in range(dim):
        value = value + math.sin(x[i]) * (math.sin(i * x[i] ** 2 / math.pi)) ** (2 * m)
    
    value = -value

    return value


def create_neigh(bitstring, pos):
    new_neigh = bitstring.copy()
    
    if new_neigh[pos] == 0:
        new_neigh[pos] = 1

    else:

        new_neigh[pos] = 0
    
    return new_neigh


def first_improve(bitstring, fct):
    indexes = list(range(length))
    current_value = fct(decode(bitstring))

    while indexes:
        index = choice(indexes)
        candidate = create_neigh(bitstring, index)
        indexes.remove(index)

        if fct(decode(candidate)) < current_value:

            return candidate
    
    return bitstring



def best_improve(bitstring, fct):
    best = bitstring.copy()

    for i in range(length):
        candidate = create_neigh(bitstring, i)
        if fct(decode(candidate)) < fct(decode(best)):
            best = candidate

    return best


    

def hill_climbing(fct, improve_meth):
    t = 0
    best = [choice([0, 1]) for _ in range(length)]
    while  t <= 100:
        isLocal = False
        candidate = [choice([0, 1]) for _ in range(length)]

        while isLocal == False:
            neighbour = improve_meth(candidate, fct)
            if fct(decode(neighbour)) < fct(decode(candidate)):
                candidate = neighbour
            
            else:

                isLocal = True
        
        t = t + 1

        if fct(decode(candidate)) < fct(decode(best)):
            best = candidate
    
    return best

def simulated_annealing(fct):
    temp = 1000
    candidate = [choice([0, 1]) for _ in range(length)]
    best = candidate.copy()

    while temp >= 0.01:
        t = 0
        while t <= length:
            neighbour = create_neigh(candidate, choice(range(length)))
            
            if fct(decode(neighbour)) < fct(decode(candidate)):
                candidate = neighbour
            
            else:

                if random() < math.exp(-math.fabs(fct(decode(neighbour)) - fct(decode(candidate))) / temp):
                    candidate = neighbour
            
            if fct(decode(candidate)) < fct(decode(best)):
                best = candidate.copy()

            t = t + 1
        
        temp = temp * 0.9

    return best

         
    

def decode(bitstring):
    global length
    global dimension

    decoded = [0 for _ in range(dimension)]
    index = 0

    for i in range(length):
        decoded[index] = decoded[index] * 2
        decoded[index] = decoded[index] + bitstring[i]

        if i != 0 and i % (length / dimension) == length / dimension - 1:
            index = index + 1
        
    for i in range(index):
        decoded[i] = decoded[i] * (b - a) / (2**int(length / dimension) - 1) + a
        
    return decoded


def put_data(aa, bb, c, d):
    global length
    global dimension
    global a
    global b
    global prec

    a = aa
    b = bb
    dimension = c
    prec = d
    length = math.ceil(math.log2((b - a) * 10 ** prec)) * dimension


def test_FIHC(fct, file_name):
    results = []
    mini = 10000
    start = timer()
    with open(file_name, "a") as file:
        file.write(f"Function dimenssion: {dimension}\n")
        for _ in range(30):
            x = hill_climbing(fct, first_improve)
            val = fct(decode(x))
            results.append(val)
            print(val)
            file.write(f"{val}, ")
            if val < mini:
                mini = val
        
        end = timer()
        st_dev = numpy.std(results)
        avg = numpy.mean(results)
        print(f"mini {mini}")
        file.write(f"\n MINIMUM: {mini}\n TIME: {(end - start) / 30}\n")
        file.write(f"Standard Deviation: {st_dev}\n")
        file.write(f"Avg result: {avg}\n\n")

def test_BIHC(fct, file_name):
    global dimension
    results = []
    mini = 10000
    start = timer()
    with open(file_name, "a") as file:
        file.write(f"Function dimenssion: {dimension}\n")
        for _ in range(30):
            x = hill_climbing(fct, best_improve)
            val = fct(decode(x))
            results.append(val)
            print(val)
            file.write(f"{val}, ")
            if val < mini:
                mini = val
            if dimension == 30:
                break
        
        end = timer()
        st_dev = numpy.std(results)
        avg = numpy.mean(results)
        print(f"mini {mini}")
        file.write(f"\n MINIMUM: {mini}\n TIME: {(end - start) / 30}\n")
        file.write(f"Standard Deviation: {st_dev}\n")
        file.write(f"Avg result: {avg}\n\n")

                
def test_SA(fct, file_name):
    results = []
    mini = 10000
    start = timer()
    with open(file_name, "a") as file:
        file.write(f"Function dimenssion: {dimension}\n")
        for _ in range(30):
            x = simulated_annealing(fct)
            val = fct(decode(x))
            results.append(val)
            print(val)
            file.write(f"{val}, ")
            if val < mini:
                mini = val
        
        end = timer()
        st_dev = numpy.std(results)
        avg = numpy.mean(results)
        print(f"mini {mini}")
        file.write(f"\n MINIMUM: {mini}\n TIME: {(end - start) / 30}\n")
        file.write(f"Standard Deviation: {st_dev}\n")
        file.write(f"Avg result: {avg}\n\n")


#file_name = "Rastrigin.txt"
#put_data(-5.12, 5.12, 5, 2)
#test_BIHC(Rastrigin, file_name)
#test_FIHC(Rastrigin, file_name)

#put_data(-5.12, 5.12, 10, 2)
#test_BIHC(Rastrigin, file_name)
#test_FIHC(Rastrigin, file_name)

#put_data(-5.12, 5.12, 30, 2)
#test_BIHC(Rastrigin, file_name)
#test_FIHC(Rastrigin, file_name)


#file_name = "DeJong.txt"
#put_data(-5.12, 5.12, 5, 2)
#test_BIHC(DeJong, file_name)
#test_FIHC(DeJong, file_name)

#put_data(-5.12, 5.12, 10, 2)
#test_BIHC(DeJong, file_name)
#test_FIHC(DeJong, file_name)

#put_data(-5.12, 5.12, 30, 2)
#test_BIHC(DeJong, file_name)
#test_FIHC(DeJong, file_name)


#file_name = "Michalewicz.txt"
#put_data(0, math.pi, 5, 2)
#test_BIHC(Michalewicz, file_name)
#test_FIHC(Michalewicz, file_name)

#put_data(0, math.pi, 10, 2)
#test_BIHC(Michalewicz, file_name)
#test_FIHC(Michalewicz, file_name)

#put_data(0, math.pi, 30, 2)
#test_BIHC(Michalewicz, file_name)
#test_FIHC(Michalewicz, file_name)

#file_name = "Schwefel.txt"
#put_data(-500, 500, 5, 2)
#test_BIHC(Schwefel, file_name)
#test_FIHC(Schwefel, file_name)

#put_data(-500, 500, 10, 2)
#test_BIHC(Schwefel, file_name)
#test_FIHC(Schwefel, file_name)

#put_data(-500, 500, 30, 2)
#test_BIHC(Schwefel, file_name)
#test_FIHC(Schwefel, file_name)

#file_name = "Simulated.txt"
#put_data(-5.12, 5.12, 5, 2)
#test_SA(Rastrigin, file_name)
#put_data(-5.12, 5.12, 10, 2)
#test_SA(Rastrigin, file_name)
#put_data(-5.12, 5.12, 30, 2)
#test_SA(Rastrigin, file_name)

#file_name = "Simulated1.txt"
#put_data(0, math.pi, 5, 2)
#test_SA(Michalewicz, file_name)
#put_data(0, math.pi, 10, 2)
#test_SA(Michalewicz, file_name)
#put_data(0, math.pi, 30, 2)
#test_SA(Michalewicz, file_name)

#file_name = "Simulated2.txt"
#put_data(-500, 500, 5, 2)
#test_SA(Schwefel, file_name)
#put_data(-500, 500, 10, 2)
#test_SA(Schwefel, file_name)
#put_data(-500, 500, 30, 2)
#test_SA(Schwefel, file_name)

file_name = "Simulated3.txt"
put_data(-5.12, 5.12, 5, 2)
test_SA(DeJong, file_name)
put_data(-5.12, 5.12, 10, 2)
test_SA(DeJong, file_name)
put_data(-5.12, 5.12, 30, 2)
test_SA(DeJong, file_name)
