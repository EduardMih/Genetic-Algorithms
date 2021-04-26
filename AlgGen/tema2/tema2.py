


import math
import numpy
from random import choice
from random import random
from random import randint
from random import uniform
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

def mutation(pop):
    mut_prob = 0.001
    pop_size = 100
    
    for i in range(pop_size):
        for j in range(length):
            if uniform(0, 1) < mut_prob:
                if pop[i][j] == 0:
                    pop[i][j] = 1
            
                else:

                    pop[i][j] = 0

    return pop


def fitness(individ, fct):
    global dimension

    Epsilon = 0.1
    result = fct(decode(individ))

    if fct == Schwefel:
        result = result + 418.9829 * dimension

    if fct == Michalewicz:
        result = -1 * result

    fitness_value = 1 / (result + Epsilon)

    return fitness_value

def get_key(prob):

    return prob[1]

def crossover(pop):
    pop_size = 100
    new_pop = []
    prob = []

    for i in range(pop_size):
        prob.append((pop[i], uniform(0, 1)))
    
    sorted_prob = sorted(prob, key=get_key)

    i = 0

    while sorted_prob[i][1] < 0.4:
        c1 = sorted_prob[i][0]
        c2 = sorted_prob[i + 1][0]
        index = randint(1, length - 1)
        
        aux = c1[index:]
        c1 = c1[:index] + c2[index:]
        c2 = c2[:index] + aux

        new_pop.append(c1)
        new_pop.append(c2)

        i = i + 2


    while i < pop_size:
        new_pop.append(sorted_prob[i][0])
        i = i + 1

    
    return new_pop



def selection(pop, fct):
    pop_size = 100
    eval = [0] * pop_size
    p = [0] * pop_size
    q = [0] * pop_size
    t = 0
    new_pop = []

    for i in range(pop_size):
        eval[i] = fitness(pop[i], fct)
        t = t + eval[i]


    for i in range(pop_size):
        p[i] = eval[i] / t

    q[0] = 0

    for i in range(pop_size - 1):
        q[i + 1] = q[i] + p[i]

    for i in range(pop_size):
        k = 0
        r = uniform(0 + 0.01, 1)

        for j in range(pop_size - 1):
            if q[j] < r and r <= q[j + 1]:
                new_pop.append(pop[j])
                k = 1
            
        if k == 0:
            new_pop.append(pop[pop_size - 1])

    return new_pop



def evaluate_population(pop, fct):
    pop_size = 100
    i = 0
    fittest = pop[0]
    mini = fct(decode(fittest))

    while i < pop_size:
        individ = pop[i]
        result = fct(decode(individ))

        if result < mini:
            mini = result
            fittest = individ
        
        i = i + 1

    return fittest

def GA(fct):
    generation = 0
    pop_size = 100
    pop = [[choice([0, 1]) for _ in range(length)] for _ in range(pop_size)]
    best = evaluate_population(pop, fct)

    while generation < 1000:
        pop = selection(pop, fct)
        pop = mutation(pop)
        pop = crossover(pop)
        cand = evaluate_population(pop, fct)

        if fct(decode(cand)) < fct(decode(best)):
            best = cand

        generation = generation + 1

    return best
    



def test_GA(fct, file_name):
    mini = 100000000
    results = []

    with open(file_name, "a") as file:
        start = timer()
        file.write(f"For dimension {dimension}:\n")

        for _ in range(30):
            x = GA(fct)
            value = fct(decode(x))
            results.append(value)
            print(value)
            file.write(f"{value}, ")
            if value < mini:
                mini = value

        end = timer()
        st_dev = numpy.std(results)
        avg = numpy.mean(results)
        print(f"mini: {mini}")

        file.write(f"\nMinim: {mini}\n")
        file.write(f"Timp mediu: {(end - start) / 30}\n")
        file.write(f"Standard deviation: {st_dev}\n")
        file.write(f"Avg. result: {avg}\n\n")


#file_name = "Rastrigin.txt"
#put_data(-5.12, 5.12, 5, 2)
#test_GA(Rastrigin, file_name)

#put_data(-5.12, 5.12, 10, 2)
#test_GA(Rastrigin, file_name)

#put_data(-5.12, 5.12, 30, 2)
#test_GA(Rastrigin, file_name)

#file_name = "DeJong.txt"
#put_data(-5.12, 5.12, 5, 2)
#test_GA(DeJong, file_name)

#put_data(-5.12, 5.12, 10, 2)
#test_GA(DeJong, file_name)

#put_data(-5.12, 5.12, 30, 2)
#test_GA(DeJong, file_name)

file_name = "Michalewicz.txt"
put_data(0, math.pi, 5, 2)
test_GA(Michalewicz, file_name)

put_data(0, math.pi, 10, 2)
test_GA(Michalewicz, file_name)

put_data(0, math.pi, 30, 2)
test_GA(Michalewicz, file_name)


#file_name = "Schwefel.txt"
#put_data(-500, 500, 5, 2)
#test_GA(Schwefel, file_name)

#put_data(-500, 500, 10, 2)
#test_GA(Schwefel, file_name)

#put_data(-500, 500, 30, 2)
#test_GA(Schwefel, file_name)
