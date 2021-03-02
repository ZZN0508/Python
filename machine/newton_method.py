# -*- coding: utf-8 -*-
# @Time : 2020/11/2 19:46
# @Author : Zhining Zhang
# @site :  
# @File : newton_method.py
# @main : 使用牛顿法求逻辑回归
# @Software: PyCharm

# 导入模块
import xlrd
import matplotlib.pyplot as plt
from numpy import *

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
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
    data_tes=[]
    for i in range(len(list_price)):
        if(list_score[i]<7):
            dataMat.append([1,list_price[i],list_score[i]]);
            labelMat.append(0)
            data_tes.append([list_price[i],list_score[i],0])
        else:
            dataMat.append([1,list_price[i], list_score[i]]);
            labelMat.append(1)
            data_tes.append([list_price[i], list_score[i], 1])

    return dataMat,labelMat;

 #sigmoid函数
def sigmoid(inX):
    return 1.0/(1+exp(-inX))

#牛顿法求梯度下降
def stocGradAscent1(dataMat, labelMat):
    dataMatrix=mat(dataMat)#将读取的数据转换为矩阵 275*3
    classLabels=mat(labelMat)
    m,n=shape(dataMatrix)# 获取dataMatrix的列数和行数 275,3
    weights = mat(zeros(n))#设置初始的参数，并都赋默认值为1。注意这里权重以矩阵形式表示三个参数。
    # 求原函数
    h = sigmoid(weights * dataMatrix.T)  # h(x)
    # 计算梯度(一阶偏导)
    gradient = (h - classLabels) * dataMatrix / classLabels.size;
    #求 Hessian 矩阵 求二阶偏导
    t = multiply(h, (1 - h));
    M = mat(dataMatrix) / classLabels.size;
    for i in range(weights.size):
        M[:, i] = multiply(M[:, i], t.T)
    piandao = dataMatrix.T * M;
    #开始迭代
    for j in range(100): #迭代
        try:
            weights=weights-linalg.pinv((piandao.I*linalg.pinv(gradient)));# x(n+1)=xn-f'(x)/f''(x)
        except:
            return weights.T;
    return weights.T

#画出最终分类的图
def plotBestFit(weights):
    dataMat,labelMat=data_settle()#获取已有数据的坐标，以及对应的值
    dataArr = array(dataMat)
    n = shape(dataArr)[0]# 获取散点的个数
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    # 对读取的坐标进行分类，函数值为1的放到cord1，为0的放到cord2
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    # 标出函数值为1的点为红色，函数值为0的为绿色
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(0.0, 50.0, 0.1)
    y = (-float(weights[0]) - (float(weights[1]) * x)) / float(weights[2]);  # ax1+bx2+c=0化解为x1=(-c-bx2)/a;
    ax.plot(x, y)
    plt.title('2017年--2018年中国好电影与烂电影的情况分布图')
    plt.xlabel('票房')
    plt.ylabel('评分')
    plt.show()

    #ax.plot(new_x,y_nihe,c='yellow')


def main():
    dataMat, labelMat = data_settle()
    weights=stocGradAscent1(dataMat, labelMat)
    print(weights)
    plotBestFit(weights)
if __name__=='__main__':
    main()

