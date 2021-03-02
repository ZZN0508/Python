# -*- coding: utf-8 -*-
# @Time : 2020/11/6 9:03
# @Author : Zhining Zhang
# @site :  
# @File : regularization_line.py
# @main : 线性逻辑回归
# @Software: PyCharm

import xlrd
import matplotlib.pyplot as plt
from numpy import *

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.subplots_adjust(left=None,bottom=None,right=None, top=None,wspace=0.5,hspace=1);
# 读取数据（这里只有两个特征）, 是由X1和X2，y组成
def data_settle():
    # 打开文件方式1：
    work_book = xlrd.open_workbook('时光网.xlsx')
    sheets_name = work_book.sheet_by_name('Sheet1')
    list_score=[];
    list_price=[];
    data_col = [sheets_name.col_values(i) for i in range(sheets_name.ncols)]
    del(data_col[1][0])
    del(data_col[2][0])
    del(data_col[5][0])
    list_name=data_col[1];
    for i in data_col[2]:
        list_score.append(float(i));

    for i in data_col[5]:
        if '亿' in i:
            list_price.append(float(i.replace("亿","")));
        elif '万' in i :
            temp=i.replace("万","");
            list_price.append(float(temp)/10000);
    dataMat=[];
    labelMat=[];
    for i in range(len(list_price)):
        if(list_score[i]<7):
            dataMat.append([1,list_price[i],list_score[i]]);
            labelMat.append(0)
        else:
            dataMat.append([1,list_price[i], list_score[i]]);
            labelMat.append(1)
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
    weights1 = ones((n, 1))  # 设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    weights2 = ones((n, 1))  # 设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    maxCycles=m*2#设置迭代的次数，一般看实际数据进行设定，有些可能200次就够了
    # 惩罚系数
    learningRate = 0.01 / m
    for j in range(maxCycles): #迭代
        dataIndex=[i for i in range(m)] # 生成下标
        for i in range(m): #随机遍历每一行
            alpha=4/(1+j+i)+0.0001  #随迭代次数增加，权重变化越小。
            randIndex=int(random.uniform(0,len(dataIndex)))  #随机抽样，返回dataIndex下标数组中的任意值
            h=sigmoid(sum(dataMatrix[randIndex]*weights));# sigmoid(X(i)*θ)
            error=h-classLabels[randIndex];# 用sigmoid函数值减去实际的函数值，求得差值
            #weights=weights-alpha*error*dataMatrix[randIndex].transpose();# θ=θ-α(h(x)-y)*X.T
            weights = weights - alpha * error * dataMatrix[randIndex].transpose();  # θ=θ-α(h(x)-y)*X.T

            regular1 = learningRate
            first_value=weights[0];
            weights1 = weights - alpha * error * dataMatrix[randIndex].transpose() + regular1;  # θ=θ-α(h(x)-y)*X.T
            weights1[0]=first_value;

            regular2 = learningRate * 2 * weights
            weights2 = weights - alpha * error * dataMatrix[randIndex].transpose() + regular2;  # θ=θ-α(h(x)-y)*X.T
            weights2[0] = first_value;

            del(dataIndex[randIndex]) #去除已经抽取的样本

    return weights.getA(),weights1.getA(),weights2.getA();

#画出最终分类的图
def plotBestFit(weights,weights1,weights2):

    dataMat,labelMat=data_settle()
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
    x = arange(0.0, 50.0, 0.1)
    y1 = (-weights[0]-weights[1]*x)/weights[2]
    y2 = (-weights1[0]-weights1[1]*x)/weights1[2]
    y3 = (-weights2[0]-weights2[1]*x)/weights2[2]
    lin1, = plt.plot(x, y1, color='yellow')
    lin2, = plt.plot(x, y2, color='red')
    lin3, = plt.plot(x, y3, color='blue')
    plt.legend(handles=[lin1, lin2,lin3], labels=['原始图像', '正则化1', '正则化2'])
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

if __name__=='__main__':
    dataMat, labelMat = data_settle()
    print(dataMat)
    print(labelMat)
    weights,weights1,weights2 = stocGradAscent1(dataMat, labelMat)
    plotBestFit(weights,weights1,weights2)