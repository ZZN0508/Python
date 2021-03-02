# -*- coding: utf-8 -*-
# @Time : 2020/12/1 9:53
# @Author : Zhining Zhang
# @site :  
# @File : __init__.py.py
# @main : 
# @Software: PyCharm
import numpy as np;
import operator
from os import listdir

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createDataSet():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

if __name__ == '__main__':
   a = np.array([[1],[2],[3]])
   b = (2,3,4);
   #先进行横向拉伸共拉伸4次，再以刚才横向拉伸的结果为基准进行纵向拉伸共拉伸3次，最后以纵向拉伸为基准进行纵向拉伸共拉伸2次
   # b=(x1,x2,x3,x4,....,xn);先进行横向拉伸共拉伸xn次,再以刚才横向拉伸的结果为基准进行纵向拉伸共拉伸xn-1次,....,再以刚才横向拉伸的结果为基准进行纵向拉伸共拉伸x1次
   print(np.tile(a,b))
