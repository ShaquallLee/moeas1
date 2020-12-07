#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file:
# @time: 2020/10/9 0009 17:52
# @desc: 根据Pareto前沿计算参考点
import multiprocessing

import numpy as np
import re

from utils.common import fitness_function
from config import *
from utils.pfget import get_pflist


def get_referencepoint(pf):
    '''
    根据Pareto front 计算参考点
    :param pf:
    :return:
    '''
    pf = np.array(pf)
    reference_point = []
    for i in range(len(pf[0])):
        reference_point.append(max(pf[:, i]))
    return list(np.array(reference_point)*1.1)

def get_referencepoint1(pf, problem, name):
    # mypf = readPareto4Txt(name)
    print('starting……')
    maxfit = -float('inf')
    maxpoint= [-10,-10,-10]
    for pfi in pf:
        minfit = float('inf')
        for i in range(len(problem.pop)):
            f1 = fitness_function(problem.pop[i].pop_fitness, problem.pop[i].namda, problem.ideal_fitness)
            f2 = fitness_function(pfi, problem.pop[i].namda, problem.ideal_fitness)
            # print(f1, f2)
            if f1< minfit+f2:
                minfit = f1-f2
        if minfit > maxfit:
            maxfit = minfit
            maxpoint = pfi
    with open(f'../results/pf/{name}.txt', 'w+', encoding='utf-8') as f:
        f.write(str(maxpoint))
    print('写入成功')

def get_referencepoint2(name):
    '''
    从文件中读取参考点
    '''
    with open(f'../results/pf/{name}.txt', 'r', encoding='utf-8') as f:
        s = f.read()
        res = re.findall('\[([\d]+.[\d]*), ([\d]+.[\d]*), ([\d]+.[\d]*)]', s)
    return list(map(lambda x:float(x)*1.1, res[0]))


def count_referencepoint():
    pool = multiprocessing.Pool(processes=16)
    for i in range(len(problems)):
        name = problems_name[i]
        model = models[0](problem=problems[i])
        model.execute()
        if i<7:
            pf = get_pflist(f'../pf_files/n10000/{name}.txt')
        else:
            pf = get_pflist(f"../pf_files/wfg-pf/{name}.3D.pf")
        pool.apply_async(get_referencepoint1, (pf, model, name,))
    pool.close()
    pool.join()
    print('运行结束')

if __name__ == '__main__':
    # count_referencepoint()
    get_referencepoint2('DTLZ2')