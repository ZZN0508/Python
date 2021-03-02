# ----------------------------------------------------
# Copyright (c) 2017, Wray Zheng. All Rights Reserved.
# Distributed under the BSD License.
# ----------------------------------------------------

# -*- coding: utf-8 -*-

import numpy as np

DEBUG = False

#############################################
# 调试信息输出
#############################################
def debug(*args, **kwords):
    if DEBUG:
        print(*args, **kwords)


#############################################
# sigmoid 函数（Y = 1 的概率)
#############################################
def sigmoid(theta, X):
    result = 1.0 / (1 + np.exp(-theta * X.T))
    return result


#############################################
# 计算梯度
# X 为特征矩阵，Y 为标签，theta 为参数
#############################################
def gradient(X, Y, theta):
    return (sigmoid(theta, X) - Y) * X / Y.size


#############################################
# 计算 Hessian 矩阵 求二阶偏导
# X 为特征矩阵，Y 为标签，theta 为参数
#############################################
def hessianMatrix(X, Y, theta):
    print("开始了")
    print(X)
    print(Y)
    print(theta)
    print("结束了")
    h = sigmoid(theta, X)
    print(h)
    t = np.multiply(h, (1-h))
    M = np.mat(X) / Y.size
    for i in range(theta.size):
        M[:,i] = np.multiply(M[:,i], t.T)
    return X.T * M


#############################################
# 牛顿法估计参数
# X 为特征矩阵，Y 为标签，iterNum 为迭代次数
#############################################
def newtonMethod(X, Y, iterNum=10):

    # 在矩阵 X 的第一列插入 1
    X = np.insert(X, 0, 1, 1)
    # m 是训练样本数，n-1 是样本的特征数
    m, n = X.shape
    # 初始化 theta 值
    theta = np.mat(np.zeros(n))

    # 迭代求解theta
    for iterIndex in range(iterNum):
        g = gradient(X, Y, theta)
        H = hessianMatrix(X, Y, theta)
        theta -= (H.I * g.T).T
        debug("theta({}):\n{}\n".format(iterIndex + 1, theta))

    return theta


#############################################
# 正则化牛顿法估计参数
# X 为特征矩阵，Y 为标签，iterNum 为迭代次数
#############################################
def regularizedNewtonMethod(X, Y, iterNum=10):
    # 在矩阵 X 的第一列插入 1
    X = np.insert(X, 0, 1, 1)
    # m 是训练样本数，n-1 是样本的特征数
    m, n = X.shape
    # 初始化 theta 值
    theta = np.mat(np.zeros(n))
    # 惩罚系数
    lambda_ = 0.01 / Y.size
    # hessian 矩阵正则项
    A = np.eye(theta.size)
    A[0,0] = 0

    # 迭代求解theta
    for iterIndex in range(iterNum):
        g = gradient(X, Y, theta) + lambda_ * theta
        H = hessianMatrix(X, Y, theta) + lambda_ * A
        theta -= (H.I * g.T).T
        debug("theta({}):\n{}\n".format(iterIndex + 1, theta))

    return theta


#############################################
# 梯度下降法估计参数
# X 是样本特征矩阵，每一行表示一个样本
# Y 是样本 X 中对应的标签，数组类型
# alpha 表示步长
#############################################
def gradientDescent(X, Y, alpha=0.001):
    # 在矩阵 X 的第一列插入 1
    X = np.insert(X, 0, 1, 1)
    # m 是训练样本数，n-1 是样本的特征数
    m, n = X.shape
    # 初始化 theta 值
    theta = np.mat(np.zeros(n))

    # 迭代求解theta
    for i in range(200000):
        theta -= alpha * gradient(X, Y, theta)

    debug("theta:", theta)
    return theta


#############################################
# 正则化的梯度下降法估计参数
# X 是样本特征矩阵，每一行表示一个样本
# Y 是样本 X 中对应的标签，数组类型
# alpha 表示步长
#############################################
def regularizedGradientDescent(X, Y, alpha=0.001):
    # 在矩阵 X 的第一列插入 1
    X = np.insert(X, 0, 1, 1)
    # m 是训练样本数，n-1 是样本的特征数
    m, n = X.shape
    # 初始化 theta 值
    theta = np.mat(np.zeros(n))
    # 惩罚系数
    lambda_ = 0.01 / Y.size

    # 迭代求解theta
    for i in range(200000):
        theta -= alpha * gradient(X, Y, theta)
        theta[0,1:] -= lambda_ * theta[0,1:]

    debug("theta:", theta)
    return theta


#############################################
# 预测样本对应 Y=1 的概率
# X 是测试样本矩阵
# theta 是牛顿法估计出的参数
#############################################
def predict(X, theta):
    # 在矩阵 X 的第一列插入 1
    X = np.insert(X, 0, 1, 1)
    # 计算 X 样本对应的 Y = 1 的概率
    predictedY = np.array(sigmoid(theta, X)).flatten()
    return predictedY
