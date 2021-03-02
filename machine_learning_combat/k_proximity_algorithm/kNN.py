# -*- coding: utf-8 -*-
# @Time : 2020/12/1 9:53
# @Author : Zhining Zhang
# @site :  
# @File : kNN.py
# @main : 
# @Software: PyCharm
import numpy as np;
import operator as op;


def createDataSet():
    '''
    这是一个样本集
    :return: 返回样本集数据group和样本集的标签lables
    '''
    group = np.array([
        [1.0, 1.1],
        [1.0, 1.0],
        [0, 0],
        [0, 0.1]
    ])
    labels = ['A', 'A', 'B', 'B'];
    return group, labels;


def classify0(inX, dataSet, labels, k):
    '''
    用于求k-近邻算法
    :param inX: 需要分类的向量
    :param dataSet: 训练样本集
    :param labels: 样本标签向量
    :param k: 表示用于选择最近邻居的数量
    :return: 返回发生频率最高的元素标签
    '''
    dataSetSize = dataSet.shape[0];#获取训练集的个数
    '''
    Numpy的tile()函数，就是将原矩阵横向、纵向地复制。tile是瓷砖的意思，顾名思义，这个函数就是把数组像瓷砖一样铺展开来。
    tile(A, reps):A代表array类型的向量，reps表示将A在每个轴上的重复reps次数。
    例子：  a = np.array([[1],[2],[3]])
           b = (2,3,4);
           #先进行横向拉伸共拉伸4次，再以刚才横向拉伸的结果为基准进行纵向拉伸共拉伸3次，最后以纵向拉伸为基准进行纵向拉伸共拉伸2次
           # b=(x1,x2,x3,x4,....,xn);先进行横向拉伸共拉伸xn次,再以刚才横向拉伸的结果为基准进行纵向拉伸共拉伸xn-1次,....,再以刚才横向拉伸的结果为基准进行纵向拉伸共拉伸x1次
           [[1]      [[1 1 1 1]     [[1 1 1 1]       [[[1 1 1 1]  [[1 1 1 1]
            [2]       [2 2 2 2]      [2 2 2 2]         [2 2 2 2]   [2 2 2 2]
            [3]]      [3 3 3 3]]     [3 3 3 3]         [3 3 3 3]   [3 3 3 3] 
                                     [1 1 1 1]         [1 1 1 1]   [1 1 1 1]
                                     [2 2 2 2]         [2 2 2 2]   [2 2 2 2]  
                                     [3 3 3 3]         [3 3 3 3]   [3 3 3 3] 
                                     [1 1 1 1]         [1 1 1 1]   [1 1 1 1]
                                     [2 2 2 2]         [2 2 2 2]   [2 2 2 2]  
                                     [3 3 3 3]]        [3 3 3 3]]  [3 3 3 3]]]
           print(np.tile(a,b))
    '''
    # 根据距离公式计算d=[(xA-xB)^2+(xA'-xB')]^1/2
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet;#j将inX纵向拉伸dataSetSize次，再减去训练集，主要的目的是计算待分类向量和训练集各元素的差
    sqDiffMat = diffMat ** 2;#
    sqDistances = sqDiffMat.sum(axis=1);
    distances = sqDistances ** 0.5;
    #对上面计算的距离d从小到大排列，提取其对应的index(索引)，然后返回给sortedDistIndicies
    sortedDistIndicies = distances.argsort();
    classCount = {};
    # 计算距离最近的k个元素都是什么标签，{标签：符合的个数}
    for i in range(k):
        votoIlabel = labels[sortedDistIndicies[i]];
        classCount[votoIlabel] = classCount.get(votoIlabel, 0) + 1;
    # 对刚刚得到的距离最近的k个元素进行m排序，主义以value排序即得到的是符合个数从大道小
    sortedClassCount = sorted(classCount.items(),
                              key=op.itemgetter(1),
                              reverse=True);
    return sortedClassCount[0][0];#返回符合个数最多的


if __name__ == '__main__':
    import datetime;
    delta = datetime.datetime.strptime("2019/1/11 21:12:34", '%Y/%m/%d %H:%M:%S')-\
            datetime.datetime.strptime("2019/7/8  17:16:57", '%Y/%m/%d %H:%M:%S')
    print(delta)
    # group, labels = createDataSet();
    # print(classify0([0, 0], group, labels, 3))
