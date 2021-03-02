# ----------------------------------------------------
# Copyright (c) 2017, Wray Zheng. All Rights Reserved.
# Distributed under the BSD License.
# ----------------------------------------------------

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from logistic import *

#############################################
# 以不同样式绘制两类样本点
#############################################
def plotsample(X, Y):
    positive = []
    negative = []
    for i in range(len(Y)):
        if Y[i] == 1: positive.append([X[i,0], X[i,1]])
        else: negative.append([X[i,0], X[i,1]])
    positive = np.array(positive)
    negative = np.array(negative)

    plt.plot(positive[:,0], positive[:,1], 'rx')
    plt.plot(negative[:,0], negative[:,1], 'bo')

# 载入样本数据
X = np.loadtxt("ex4x.dat")
Y = np.loadtxt("ex4y.dat")
matX = np.mat(X)
matY = np.mat(Y)

# 估计参数
theta1 = newtonMethod(matX, matY)
theta2 = regularizedNewtonMethod(matX, matY)

# 根据得到的参数，计算分界线
theta1 = np.array(theta1).flatten()
theta2 = np.array(theta2).flatten()
b1, a1 = -theta1[:2] / theta1[2]
b2, a2 = -theta2[:2] / theta2[2]
f1 = lambda x: a1 * x + b1
f2 = lambda x: a2 * x + b2
x = [X[:,0].min(), X[:,1].max()]
y1 = [f1(i) for i in x]
y2 = [f2(i) for i in x]

# 绘制样本点
plotsample(X, Y)

# 绘制分界线
plt.plot(x, y1, c='blue', label="nomal")
plt.plot(x, y2, c='red', label="regularized")
plt.legend(loc="lower right")
plt.xlim(X[:,0].min()-0.1, X[:,0].max()+0.1)
plt.ylim(X[:,1].min()-0.1, X[:,1].max()+0.1)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Logistic Regression")

plt.show()
