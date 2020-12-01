import random
import numpy as np

def normal_random(m,f, n):
    '''
    正态分布随机取得n个随机数
    :param m:
    :param f:
    :param n:
    :return:
    '''
    return np.random.normal(m, f, n)

def random_getI(arr):
    '''
    根据每个元素的概率随机取得一个元素
    :param arr: 记录每个元素被选的概率
    :return:
    '''
    ran = random.random()
    i = 0
    s = arr[0]
    while ran>s and i<len(arr):
        i += 1
        s += arr[i]
    return i

# a = [0.1, 0.5, 0.4]
# i, r = random_getI(a)
# print(i, r)

