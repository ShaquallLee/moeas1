#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: moeadSaDE.py
# @time: 2020/10/29 0018 11:59
# @desc:
import math

import numpy as np
import copy
import random

from utils.countFit import evaluate
from utils.individual import Individual as ind
from utils.pfget import get_pflist
from utils.igd import get_igd
from utils.common import get_random_list,fitness_function
from utils.boundaryProcess import *
from utils.randomItem import *
from utils.mutationProcess import *

mps = [mp1, mp2, mp3]
mps_n = [2, 4, 4]

class MOEADSADE():
    def __init__(self, pf, problem):
        # 每次最大迭代的次数
        self.max_generation = 500
        # 每次最大计算fitness次数
        self.max_count_fitness = 200000
        self.nfes = 0
        # 计算邻居个数
        self.max_neighborhood_size = 20

        # 问题变量的维度
        self.n_var = 10
        # 需要解决的问题
        if 'WFG' in problem.__name__:
            self.problem = problem
            # 目标函数变量取值上下界
            self.lbound = np.array([0] * self.n_var)
            self.rbound = np.array([1] * self.n_var)
            self.pname = problem.__name__
        else:  # if 'DTLZ' in problem.__name__:
            self.problem = problem(self.n_var)
            # 目标函数变量取值上下界
            self.lbound = self.problem.xl
            self.rbound = self.problem.xu
            self.pname = self.problem.name()
        # 多目标问题的个数
        self.n_obj = 3  # self.problem.n_obj

        # 变异过程中用到的参数
        self.realb = 0.9 #从邻居还是全体成员之中选择交叉项的阈值
        self.mating_size = 2 #交叉杂交的个体数量
        # self.rate = 0.5 #更新速度
        self.limit = 2#5  # 最多被替代更新的次数

        self.learning_period = 20 # 101* self.n_var # 学习周期
        self.ns = [] # success memory
        self.nf = [] # failure memory

        self.k = 3 # 使用的策略的个数
        self.select_p = [1.0/self.k for i in range(self.k)] # 每个更新策略的被选择概率，共k个
        self.F = [] # 每个个体更新的F值，共NP个
        self.strategy_k = [] #每个个体所选择的策略，共NP个

        # 问题的种群
        self.pop_size = 300  # 种群大小
        self.unit = 33 # 3目标的时候用这个方式
        self.pop = []   # 种群个体

        # ideal point 理想点
        self.ideal_point = []
        self.ideal_fitness = []

        #pareto前沿
        self.pareto_front = pf#get_pflist('./pf_files/n10000/{}.txt'.format(self.problem.name()))

    def execute(self):
        gen = 1
        distances = []
        self.init_uniformweight()
        # print("初始化权重完成")
        self.init_neighbourhood()
        # print("初始化邻居完成")
        self.init_population()
        # print("初始化种群完成")
        dis = self.calc_distance()

        self.init_nsf()
        distances.append(dis)

        while(self.nfes<self.max_count_fitness):
            self.calc_kselect(gen)
            self.diffevolution(gen)
            if gen%25==0:
                dis = self.calc_distance()
                # print("第{}代的IGD为{}".format(gen, dis))
                distances.append(dis)
            gen += 1
        return distances

    def calc_kselect(self, gen):
        '''
        种群中每个个体依据概率选择一个变异策略
        :param gen:
        :return:
        '''
        self.F = normal_random(0.5, 0.3, self.pop_size)
        if gen >= self.learning_period:
            s = []
            for i in range(self.k):
                fm = sum([x[i] for x in self.ns])
                fz = sum([x[i] for x in self.ns]) + sum([x[i] for x in self.nf])
                s.append(float(fm)/fz)
            sums = sum(s)
            if sums!=0:
                for i in range(self.k):
                    self.select_p[i] = float(s[i])/sums
        for i in range(self.pop_size):
            self.strategy_k.append(random_getI(self.select_p))


    def init_uniformweight(self):
        '''
        初始化
        :return:
        '''

        if self.n_obj == 2:
            for i in range(self.pop_size):
                pop = ind()
                a = (1.0*i)/(self.pop_size-1)
                pop.namda.append(a)
                pop.namda.append(1-a)
                self.pop.append(pop)
        elif self.n_obj == 3:
            for i in range(self.unit):
                for j in range(self.unit):
                    if i+j <= self.unit:
                        pop = ind()
                        pop.vector.append(i)
                        pop.vector.append(j)
                        pop.vector.append(self.unit-i-j)
                        for k in range(self.n_obj):
                            pop.namda.append((1.0*pop.vector[k])/self.unit)
                        self.pop.append(pop)
            self.pop_size = len(self.pop)

    def init_neighbourhood(self):
        '''
        初始化邻居
        :return:
        '''
        distances = []
        for i in range(self.pop_size):
            idis = []
            for j in range(self.pop_size):
                idis.append((math.sqrt(sum((np.array(self.pop[i].namda) - np.array(self.pop[j].namda)) ** 2)), j))
            res = sorted(idis, key=lambda x: x[0])
            self.pop[i].neighbor = [x[1] for x in res[1:self.max_neighborhood_size + 1]]

    def init_population(self):
        '''
        初始化种群
        :return:
        '''
        self.ideal_fitness = [float('inf'), float('inf'), float('inf')]
        self.ideal_point = [None, None, None]
        for i in range(self.pop_size):
            # initial pop and fitness
            pop = self.lbound + (self.rbound - self.lbound) * np.random.rand(self.n_var)
            self.pop[i].pop_x = pop
            self.pop[i].pop_fitness = evaluate(self, pop)
            self.nfes += 1
            # update reference point
            for j in range(self.n_obj):
                if self.pop[i].pop_fitness[j] < self.ideal_fitness[j]:
                    self.ideal_fitness[j] = self.pop[i].pop_fitness[j]
                    self.ideal_point[j] = copy.copy(self.pop[i].pop_x)

    def init_nsf(self):
        '''
        初始化ns和nf
        :return:
        '''
        self.ns = [[0 for i in range(self.k)] for j in range(self.learning_period)]
        self.nf = [[0 for i in range(self.k)] for j in range(self.learning_period)]

    def calc_distance(self):
        '''
        计算距离，此处计算的是反世代距离IGD
        :return:
        '''
        pop = [x.pop_fitness for x in self.pop]
        return get_igd(self.pareto_front, pop)

    def diffevolution(self, gen):
        '''
        差分进化算子
        :return:
        '''
        perm = get_random_list(self.pop_size)
        tt = []
        ff = []
        for i in range(self.pop_size):
            n = perm[i]
            type =1
            if random.random()>self.realb:
                type = 2
            child= self.diff_evo_xover2(n, type)
            # child = self.realmutation(child, 1.0/self.n_var)
            fit = evaluate(self, child)
            self.update_reference(fit)
            t, f = self.update_problem(child, n, type, fit)
            tt.append(t)
            ff.append(f)
            self.nfes += 1
        if gen > self.learning_period:
            self.ns.pop(0)
            self.ns.append(tt)
            self.nf.pop(0)
            self.nf.append(ff)
        else:
            self.ns.append(tt)
            self.nf.append(ff)


    def mating_selection(self, cid, size, type):
        '''
        变异元素选择
        :param cid:
        :param size:
        :param type:
        :return:
        '''
        if type == 1:
            return [self.pop[i] for i in random.sample(self.pop[cid].neighbor, size)]
        else:
            return random.sample(self.pop, size)

    def diff_evo_xover2(self, cid, type):
        '''
        差分进化算子
        :param cid:
        :param pop1:
        :param pop2:
        :return:
        '''
        # idx_rnd = random.randint(0, self.n_var)
        child = [-1 for i in range(self.n_var)]
        mps_i = self.strategy_k[cid]
        method = mps[mps_i]
        mps_sn = mps_n[mps_i]

        p = self.mating_selection(cid, mps_sn, type)
        for i in range(self.n_var):
            xi = method(self.pop[cid].pop_x[i], self.F[cid], p, i)
            # xi1 = bpm1(xi1, self.lbound[i], self.rbound[i])#超越边界处理
            xi = bpm3(xi, self.lbound[i], self.rbound[i])#超越边界处理
            child[i] = xi
        return child


    def realmutation(self, child, rate):
        etam = 20
        for j in range(self.n_var):
            if random.random() < rate:
                y = child[j]
                delta1 = (y-self.lbound[j])/(self.rbound[j]-self.lbound[j])
                # print("delta1=",delta1)
                delta2 = (self.rbound[j]-y)/(self.rbound[j]-self.lbound[j])
                mut_pow = 1.0/(etam+1.0)
                rnd = random.random()
                if rnd <=0.5:
                    xy = 1.0-delta1
                    val = 2.0*rnd+(1.0-2.0*rnd)*(pow(xy, (etam+1.0)))
                    # print("rnd={},xy={}".format(rnd, xy))
                    deltaq = pow(val, mut_pow)-1.0
                    # print("val={}, pow={}".format(val, mut_pow))
                else:
                    xy = 1.0-delta2
                    val = 2.0*(1.0-rnd)+2.0*(rnd-0.5)*(pow(xy, (etam+1.0)))
                    # if val == float('inf')/float('inf'):
                    #     print("xy={},rnd={}".format(xy, rnd))
                    deltaq = 1.0-pow(val,mut_pow)
                    # print("val={}, pow={}".format(val, mut_pow))
                y = y + deltaq*(self.rbound[j]-self.lbound[j])
                if y < self.lbound[j]:
                    y = self.lbound[j]
                if y > self.rbound[j]:
                    y = self.rbound[j]
                child[j] = y
        return child

    def update_reference(self, fit):
        # fit = evaluate(self, child)
        for i in range(self.n_obj):
            if fit[i] < self.ideal_fitness[i]:
                self.ideal_fitness[i] = fit[i]
                self.ideal_point[i] = fit
        return fit

    def update_problem(self, child, n, type, fit):
        '''
        更新子元素
        :param child:
        :param n:
        :param type:
        :param fit:
        :return:
        '''
        t = 0 # 记修改的次数,即好的次数
        f = 0 # 记错误的次数，即不好的次数
        if type==1:# saDE中更新使用的是整个种群，后面可以改一下看看效果
            size = self.max_neighborhood_size
        else:
            size = self.pop_size
        perm = get_random_list(size)
        for i in range(size):
            if type==1:
                k = self.pop[n].neighbor[perm[i]]
            else:
                k = perm[i]
            f1 = fitness_function(self.pop[k].pop_fitness, self.pop[k].namda, self.ideal_fitness)
            f2 = fitness_function(fit, self.pop[k].namda, self.ideal_fitness)
            if f2 < f1:
                self.pop[k].pop_x = child
                self.pop[k].pop_fitness = fit
                self.strategy_k[k] = self.strategy_k[n]
                t += 1
            else:
                f += 1

            # if t > self.limit:
            #     return 0
        return t, f
