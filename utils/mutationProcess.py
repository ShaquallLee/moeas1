import random


def mp1(pop_x, rate, pop, i):
    return pop_x + rate * (pop[0].pop_x[i] - pop[1].pop_x[i])


def mp2(pop_x, rate, pop, i):
    return pop_x + rate * (pop[0].pop_x[i] - pop[1].pop_x[i]) + rate * (pop[2].pop_x[i] - pop[3].pop_x[i])


def mp3(pop_x, rate, pop, i):
    return pop_x + random.random() * (pop[0].pop_x[i] - pop[1].pop_x[i]) + rate * (pop[2].pop_x[i] - pop[3].pop_x[i])
