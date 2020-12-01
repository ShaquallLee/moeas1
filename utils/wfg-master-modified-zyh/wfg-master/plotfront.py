#! /bin/env python
#
#  Plot solutions from a Walking Fish Group front with 3 objectives
#

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import wfg
# 画N 500个点， M 3目标的函数。
N = 500                                 # Number of points to plot
M = 3                                   # Number of objectives
kfactor = 2
lfactor = 2

k = kfactor*(M-1) #4
l = lfactor*2#4

func = wfg.WFG9

y = np.zeros((N, M))
for n in range(N):
    z = wfg.random_soln(k, l, func.__name__)
    y[n,:] = func(z, k, M)



fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(y[:,0], y[:,1], y[:,2])
plt.suptitle(func.__name__)

plt.show(block=True)
