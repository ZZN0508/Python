# -*- coding: utf-8 -*-
# @Time : 2021/1/3 16:09
# @Author : Zhining Zhang
# @site :  
# @File : tree.py.py
# @main : 决策树基础
# @Software: PyCharm
import math;
import operator;

def calcShannonEnt(dataSet):
    """

    :param dataSet: 数据集
    :return: 计算所有类别所有可能值包含的信息期望即熵
    """
    numEntries = len(dataSet);
    labelCounts={};
    # 统计各个可能结果的出现次数
    for setValue in dataSet:
        currentLable = setValue[-1];
        if currentLable not in labelCounts.keys():
            labelCounts[currentLable] = 0;
        labelCounts[currentLable] += 1;
    shannonEnt = 0.0;
    # 计算信息期望值H
    for key in labelCounts:
        # 计算选择该分类的概率
        prob = float(labelCounts[key])/numEntries;
        # 计算信息期望值
        shannonEnt -=prob * math.log(prob,2);
    return shannonEnt

def createDataSet():
    """
    生成数据
    :return: 返回训练集和特征标签名称
    """
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']];
    labels =['no surfacing','flippers'];
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    """
    按照给定特征划分数据集
    :param dataSet:待划分的数据集
    :param axis:划分数据集的某个特征
    :param value:需要返回的特征值
    :return: 返回划分结果
    """
    retDataSet = [];
    for featVec in dataSet:
        if(featVec[axis]==value):
            reducedFeatVec = featVec[:axis];
            reducedFeatVec.extend(featVec[axis+1:]);# extend合并集合
            retDataSet.append(reducedFeatVec);
    return  retDataSet;

def chooseBestFeathreToSplit(dataSet):
    """
    获取最好的划分数据集的特征
    :param dataSet: 数据集
    :return: 返回最好的划分数据集的特征索引值
    """
    numFeatures = len(dataSet[0]) - 1;
    baseEntropy = calcShannonEnt(dataSet);# 获取熵
    bestInfoGain = 0.0;# 存放最大的信息
    bestFeature = -1;# 存放最好分割的特征index
    for i in range(numFeatures):
        # 创建唯一的分类标签列表
        featList = [example[i] for example in dataSet];
        uniqueVals = set(featList);
        newEntropy = 0.0;
        # 计算每种划分方式的信息熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value);
            prob = len(subDataSet)/float(len(dataSet));
            newEntropy += prob * calcShannonEnt(subDataSet);
        infoGain = baseEntropy - newEntropy;
        # 计算最好的信息增益
        if(infoGain>bestInfoGain):
            bestInfoGain = infoGain;
            bestFeature = i;
    return bestFeature;

def majorityCnt(classList):
    """
    返回出现次数最多的分类名称
    :param classList:分类的索引标签列表
    :return:返回出现次数最多的分类名称
    """
    classCount={};
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0;
        classCount[vote]+=1;
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True);
    return sortedClassCount[0][0];

def createTree(dataSet,labels):
    """
    创建决策树
    :param dataSet: 数据集
    :param labels: 数据集中特征的标签名
    :return: 创建好的决策树
    """
    classList = [example[-1] for example in dataSet];
    if classList.count(classList[0]) == len(classList):# 判断classList的内容是否是一样的，list.count用于统计某个元素在列表中出现的次数
        return  classList[0];
    # 遍历完所有特征时返回出现次数最多的
    if len(dataSet[0]) == 1:
        return majorityCnt(classList);
    bestFeat = chooseBestFeathreToSplit(dataSet);
    bestFeatLable = labels[bestFeat];
    myTree = {bestFeatLable:{}};
    # 得到连表包含的所有属性值
    del(labels[bestFeat]);
    featValues = [example[bestFeat] for example in dataSet];
    uniqueVals = set(featValues);
    for value in uniqueVals:
        subLabels = labels[:];
        myTree[bestFeatLable][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels);
    return myTree;

def classify(inputTree,featLabels,testVec):
    """
    决策树的分类函数
    :param inputTree:树结构
    :param featLabels: 分类标签List
    :param testVec: 进行分类的
    :return:
    """
    firstStr = list(inputTree.keys())[0];
    secondDict = inputTree[firstStr];
    featIndex = featLabels.index(firstStr);# 将标签字符串转换为索引
    for key in secondDict.keys():
        if(testVec[featIndex] == key):
            if(type(secondDict[key]).__name__=='dict'):
                classLabel = classify(secondDict[key],featLabels,testVec);
            else:
                classLabel = secondDict[key];
    return classLabel;

def storeTree(inputTree,filename):
    """
    保存树结构到磁盘
    :param inputTree: 树结构
    :param filename: 存放位置
    """
    fw = open(filename,'wb+');
    fw.write(str(inputTree).encode('utf-8'))
    fw.close();
def grabTree(filename):
    """
    从磁盘读取保存的树结构
    :param filename:
    :return:
    """
    retStr = "";
    with open(filename, 'r') as f:
        retStr+=f.read();
    return eval(retStr)
    #return pickle.load(fr);

if __name__=="__main__":
    dataSet,labels = createDataSet();
    print(dataSet)
    # 根据数据0列的特征进行划分，返回0列的特征为1的对象
    print(splitDataSet(dataSet,0,1)) # [[1, 'yes'], [1, 'yes'], [0, 'no']]
    # 根据数据0列的特征进行划分，返回0列的特征为0的对象
    print(splitDataSet(dataSet, 0, 0))  # [[1, 'no'], [1, 'no']]
    print(labels)
    # 创建树
    myTree = createTree(dataSet,labels.copy());
    print(chooseBestFeathreToSplit(dataSet));# 0 表示使用0号特征值进行分割是最好的办法
    print(calcShannonEnt(dataSet))# 0.9709505944546686
    #测试决策树
    print(classify(myTree,labels,[1,0]))
    #保存
    storeTree(myTree,'classifierStorage.txt');
    print(grabTree('classifierStorage.txt'));
    # 当分类越多熵越大
    dataSet.append([1,1,'maybe']);# 有三个分类
    print(calcShannonEnt(dataSet))  # 1.4591479170272448
    dataSet.append([0, 0, 'none']);# 有四个分类
    print(calcShannonEnt(dataSet))  # 1.8423709931771088