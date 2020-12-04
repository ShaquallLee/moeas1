import random


def mp1(pop_x, rate, pop, i, CR, jrand):
    '''
    rand/1
    '''
    new_x = pop[0].pop_x[i] + rate * (pop[1].pop_x[i] - pop[2].pop_x[i])
    return using_CR(i, pop_x, new_x, CR, jrand)

def mp2(pop_x, rate, pop, i, CR, jrand):
    '''
    rand/2
    '''
    new_x= pop[0].pop_x[i] + rate * (pop[1].pop_x[i] - pop[2].pop_x[i]) + rate * (pop[3].pop_x[i] - pop[4].pop_x[i])
    return using_CR(i, pop_x, new_x, CR, jrand)

def mp3(pop_x, rate, pop, i, CR, jrand):
    '''
    current-to-rand/1
    '''
    new_x = pop_x + random.random() * (pop[0].pop_x[i] - pop_x) + rate * (pop[1].pop_x[i] - pop[2].pop_x[i])
    return new_x#using_CR(i, pop_x, new_x, CR, jrand)

def using_CR(i, pop_x, new_x, cr, jrand):
    '''
    使用CR判断是否使用交叉之后的结果
    '''
    if random.random() < cr or i == jrand:
        return new_x
    else:
        return pop_x
