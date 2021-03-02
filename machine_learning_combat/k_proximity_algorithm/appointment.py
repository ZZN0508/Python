# -*- coding: utf-8 -*-
# @Time : 2020/12/7 19:27
# @Author : Zhining Zhang
# @site :  
# @File : appointment.py
# @main : datingTestSet.txt存放了1000条数据，数据中包含
# 1、每年获得的飞行常客里程数，2、玩视频游戏所消耗的时间，3、每周消费的冰激凌公升数
# @Software: PyCharm
import numpy as np;
import matplotlib.pyplot as plt;
import kNN;
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def file2matrix(filename):
    '''
    读取特征和分类，并保存到list中
    :param filename: 文件路径名
    :return: 特征值，标签
    '''
    fr = open(filename);
    arrayOLines = fr.readlines();
    numberOFLines = len(arrayOLines)
    returnMat = np.zeros((numberOFLines,3));
    classLabelVector = [];
    index = 0;
    for line in arrayOLines:
        line = line.strip();
        listFromLine = line.split('\t');#通过\t分割各个特征值和
        returnMat[index,:] = listFromLine[0:3];#
        classLabelVector.append(int(listFromLine[-1]))
        index +=1;
    return returnMat,classLabelVector
def show_data(datingDataMat,datingLabels):
    '''
    对读取的特征和类型进行图形化
    :param datingDataMat: 特征值
    :param datingLabels: 类型
    :return:
    '''
    fig = plt.figure();
    ax = fig.add_subplot(111);
    # datingDataMat第一列为横坐标，第二列为纵坐标，
    # 16.0*np.array(datingLabels)让不同的类型大小不同
    # np.array(datingLabels)是让颜色不同
    ax.scatter(datingDataMat[:,1],datingDataMat[:,2],
               20*np.array(datingLabels),np.array(datingLabels));
    plt.xlabel('玩视频游戏所耗时间百分比')
    plt.ylabel('每周消费的冰激凌公升数')
    plt.show()

def autoNorm(dataSet):
    '''
    归一化特征值，主要是为了使得预处理的数据被限定在一定的范围内（比如[0,1]或者[-1,1]），从而消除奇异样本数据导致的不良影响。
    通过公式newValue = (oldValue-min)/(max-min);min和max分别都是训练集中的最小值和最大值
    :param dataSet:特征值是np的array类型
    :return:归一化后的特征，特征最大值和最小值的差，最小特征值
    '''
    minVals = dataSet.min(0);
    maxValue = dataSet.max(0);
    ranges = maxValue-minVals;
    # 创建于dataSet同行同列单值全为0的矩阵
    normDataSet = np.zeros(np.shape(dataSet));
    m = dataSet.shape[0];# 获取行数
    #进行归一化计算
    normDataSet = dataSet - np.tile(minVals,(m,1));# 求oldValue-min
    normDataSet = normDataSet/np.tile(ranges,(m,1));# 求(oldValue-min)/(max-min)
    return normDataSet,ranges,minVals;

def classifyPerson():
    resultList = ['不喜欢','魅力一般','极具魅力'];
    percentTats = float(input("请输入看电影玩游戏的时间"));
    ffMiles = float(input("请输入飞行公里数"));
    iceCream = float(input("请输入每年摄入的冰激凌公升数"));
    datingDataMat, datingLabels = file2matrix("k_proximity_algorithm/datingTestSet.txt");
    normDataSet, ranges, minVals = autoNorm(datingDataMat);
    inArr = np.array([ffMiles,percentTats,iceCream]);
    #(inArr-minVals)/ranges对输入的数据进行归一化
    classifierResult = kNN.classify0((inArr - minVals) / ranges, normDataSet, datingLabels, 3)
    print('您输入的内容判别该女性魅力为{}'.format(resultList[classifierResult-1]))

def datingClassTest():
    '''
    测试约会网站样本集的错误率
    :return:
    '''
    hoRatio = 0.10;
    datingDataMat, datingLabels = file2matrix("k_proximity_algorithm/datingTestSet.txt");
    normDataSet, ranges, minVals = autoNorm(datingDataMat)
    m = normDataSet.shape[0];
    numTestVecs = int(m*hoRatio);
    errorCount = 0.0;
    for i in range(numTestVecs):
        classifierResult = kNN.classify0(normDataSet[i, 0], normDataSet[numTestVecs:m, :]
                                         ,datingLabels[numTestVecs:m], 3)
        print("这个测试结果是{}，正确结果是{}".format(classifierResult,datingLabels[i]));
        if(classifierResult != datingLabels[i]):
            errorCount+=1.0;
    print("错误率为{}".format(errorCount/float(numTestVecs)));


if __name__=="__main__":
    datingClassTest();
    classifyPerson();