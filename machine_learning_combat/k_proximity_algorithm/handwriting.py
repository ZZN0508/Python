# -*- coding: utf-8 -*-
# @Time : 2020/12/23 10:29
# @Author : Zhining Zhang
# @site :  
# @File : handwriting.py
# @main : 使用k邻近算法手写识别
# @Software: PyCharm
import numpy as np;
import os;
import kNN as knn;
def img2vector(filename):
    """
    :param filename: 手写数据存放位置
    :return: 将数据转化为1x1024向量的结果
    """
    returnVect = np.zeros((1,1024));
    fr = open(filename);
    for i in range(32):
        lineStr = fr.readline();
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j]);
    return returnVect;

def handWritingClassTest():
    """
    手写数字识别系统的测试
    """
    # 获取训练集数据
    hwLables = [];# 存放训练数据
    trainingFileList = os.listdir('trainingDigits');
    m = len(trainingFileList);
    trainingMat = np.zeros((m,1024));
    for i in range(m):
        fileName = trainingFileList[i];
        fileStr = fileName.split('.')[0];
        classNumStr = int(fileStr.split('_')[0]);
        hwLables.append(classNumStr);
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileName);# 读取手写数据，并存到训练集中
    # 获取测试集数据
    testFileList = os.listdir('testDigits');
    errorCount = 0.0;
    mTest = len(testFileList);
    for i in range(mTest):
        fileName = testFileList[i];
        fileStr = fileName.split('.')[0];
        classNumStr = int(fileStr.split('_')[0]);
        vectorUnderTest = img2vector('testDigits/%s' % fileName);# 读取测试集手写数据
        classifierResult = knn.classify0(vectorUnderTest,trainingMat,hwLables,3);# 使用k邻近算法进行计算
        print("分类器返回的是:%d，真正的答案是:%d" % (classifierResult,classNumStr));
        if(classifierResult!=classNumStr):
            errorCount+=1;
    print("错误个数是%d" % errorCount);
    print("错误率%f" % (float(errorCount)/float(mTest)))


if __name__ == "__main__":
    testVector = img2vector("./trainingDigits/0_13.txt");
    print(testVector[0,])
    handWritingClassTest()