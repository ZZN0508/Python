# -*- coding: utf-8 -*-
# @Time : 2020/11/3 9:34
# @Author : Zhining Zhang
# @site :  
# @File : multiple_book_logistic_regression.py
# @main : 多项式逻辑回归
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time : 2020/10/20 10:33
# @Author : Zhining Zhang
# @site :
# @File : logistic_regression.py
# @main : 逻辑回归
# @Software: PyCharm
# -*- coding: utf-8 -*-
# 逻辑回归公式,z可以是θ.Tx
import xlrd
import matplotlib.pyplot as plt
from numpy import *

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.subplots_adjust(left=None,bottom=None,right=None, top=None,wspace=0.5,hspace=1);


# 生成数据
def data_settle():
    dataMat=[];
    labelMat=[];
    for i in range(25):
        dataMat.append([1,random.uniform(-4,-3),random.uniform(-4, 4)])
        labelMat.append(1);

        dataMat.append([1, random.uniform(4, 3), random.uniform(-4, 4)])
        labelMat.append(1);

        dataMat.append([1, random.uniform(-3, 3), random.uniform(-3, -3)])
        labelMat.append(1);

        dataMat.append([1, random.uniform(-2, 2), random.uniform(2, 4)])
        labelMat.append(1);


    for i in range(100):
        dataMat.append([1, random.uniform(-2, 2), random.uniform(-2, 2)])
        labelMat.append(0);
    return dataMat,labelMat;


 #sigmoid函数
def sigmoid(inX):
    return 1.0/(1+exp(-inX))

#改进版随机梯度上升，在每次迭代中随机选择样本来更新权重，并且随迭代次数增加，权重变化越小。
def stocGradAscent1(dataMat, labelMat):
    dataMatrix=mat(dataMat)#将读取的数据转换为矩阵 275*3
    classLabels=labelMat
    m,n=shape(dataMatrix)# 获取dataMatrix的列数和行数 275,3
    weights=ones((n,1))#设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    maxCycles=m*4#设置迭代的次数，一般看实际数据进行设定，有些可能200次就够了
    for j in range(maxCycles): #迭代
        dataIndex=[i for i in range(m)] # 生成下标
        for i in range(m): #随机遍历每一行
            alpha = 27 / (1 + j + i) + 0.0001  # 随迭代次数增加，权重变化越小。
            randIndex=int(random.uniform(0,len(dataIndex)))  #随机抽样，返回dataIndex下标数组中的任意值
            h=sigmoid(sum(dataMatrix[randIndex]*weights));# sigmoid(X(i)*θ)
            error=h-classLabels[randIndex];# 用sigmoid函数值减去实际的函数值，求得差值
            weights=weights-alpha*error*dataMatrix[randIndex].transpose();# θ=θ-α(h(x)-y)*X.T
            del(dataIndex[randIndex]) #去除已经抽取的样本
    return weights

#改进版随机梯度上升，在每次迭代中随机选择样本来更新权重，并且随迭代次数增加，权重变化越小。
def stocGradAscentss(dataMat, labelMat):
    dataMatrix=mat(dataMat)#将读取的数据转换为矩阵 275*3
    classLabels=labelMat
    m,n=shape(dataMatrix)# 获取dataMatrix的列数和行数 275,3
    weights=ones((n,1))#设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    weights1 = ones((n, 1))  # 设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    weights2 = ones((n, 1))  # 设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    maxCycles=m*2#设置迭代的次数，一般看实际数据进行设定，有些可能200次就够了
    # 惩罚系数
    learningRate = var(dataMat)
    for j in range(maxCycles): #迭代
        dataIndex=[i for i in range(m)] # 生成下标
        for i in range(m): #随机遍历每一行
            alpha=27 / (1 + j + i) + 0.0001  #随迭代次数增加，权重变化越小。
            randIndex=int(random.uniform(0,len(dataIndex)))  #随机抽样，返回dataIndex下标数组中的任意值
            h=sigmoid(sum(dataMatrix[randIndex]*weights));# sigmoid(X(i)*θ)
            error=h-classLabels[randIndex];# 用sigmoid函数值减去实际的函数值，求得差值
            #weights=weights-alpha*error*dataMatrix[randIndex].transpose();# θ=θ-α(h(x)-y)*X.T
            weights = weights - alpha * error * dataMatrix[randIndex].transpose();  # θ=θ-α(h(x)-y)*X.T

            regular1 = 1.414*learningRate*alpha* sum(identity(shape(weights)[1]))
            first_value=weights[0];
            weights1 = weights - alpha * error * dataMatrix[randIndex].transpose() + regular1;  # θ=θ-α(h(x)-y)*X.T
            weights1[0]=first_value;

            regular2 = 1/learningRate * 2 * sum(weights) *alpha
            weights2 = weights - alpha * error * dataMatrix[randIndex].transpose() + regular2;  # θ=θ-α(h(x)-y)*X.T
            weights2[0] = first_value;

            del(dataIndex[randIndex]) #去除已经抽取的样本

    return weights.getA(),weights1.getA(),weights2.getA();


#画出最终分类的图
def plotBestFit(dataMat, labelMat,weights):
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    r = weights[0]
    # 2.圆心坐标
    a, b = (weights[1], weights[2])
    theta = arange(0, 2 * pi, 0.01)
    x = a + r * cos(theta)
    y = b + r * sin(theta)
    axes = fig.add_subplot(111)
    lin0,= axes.plot(x, y,color='blue')
    plt.show()

if __name__=='__main__':
    plt.figure(figsize=(8, 8))
    dataMat, labelMat = data_settle()
    weights = stocGradAscent1(dataMat, labelMat).getA();
    plotBestFit(dataMat, labelMat,weights)