# -*- coding: utf-8 -*-
# @Time : 2021/1/16 12:29
# @Author : Zhining Zhang
# @site :  
# @File : regression_problem.py
# @main : 预测房价：回归问题
# @Software: PyCharm
from keras.datasets import boston_housing;
from keras import models,layers;
import numpy as np;
import mapping_training_process as mtp;
def getBostonData():
    """
    加载波士顿房价数据
    :return 返回测试样本和训练样本，已经测试房价和训练房价
    """
    (train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()
    # 我们有 404 个训练样本和 102 个测试样本，每个样本都有 13 个数值特征，比如人均犯罪率、每个住宅的平均房间数、高速公路可达性等。
    # 目标是房屋价格的中位数，单位是千美元。房价大都在 10 000~50 000 美元
    print(train_data.shape)# (404, 13)
    print(test_data.shape)# (102, 13)
    print(train_targets)#[15.2 42.3 50. .... 19.4 19.4 29.1]
    return  (train_data, train_targets), (test_data, test_targets)
def standardization(train_data,test_data):
    '''
    数据标准化
    :param train_data: 训练集
    :param test_data: 测试集
    :return: 标准化后的数据
    '''
    '''
    将取值范围差异很大的数据输入到神经网络中，这是有问题的。网络可能会自动适应这种
取值范围不同的数据，但学习肯定变得更加困难。对于这种数据，普遍采用的最佳实践是对每
个特征做标准化，即对于输入数据的每个特征（输入数据矩阵中的列），减去特征平均值，再除
以标准差，这样得到的特征平均值为 0，标准差为 1。用 Numpy 可以很容易实现标准化'''
    '''
    # data.mean(axis=0) 输出矩阵为一行,求每列的平均值,同理data.mean(axis=1) 输出矩阵为一列,求每行的平均值
    # data.std(axis=0) 输出矩阵为一列,求每列的标准差,同理data.std(axis=1) 输出矩阵为一列,求每行的标准差
    '''
    mean = train_data.mean(axis=0);
    train_data -=mean;
    std = train_data.std(axis=0);
    train_data /= std;
    test_data -= mean;
    test_data /= std;
    return train_data,test_data;

def modelCreat(train_data):
    """
    模型定义
    :param train_data:训练集特征值
    """
    model = models.Sequential();
    model.add(layers.Dense(64,activation='relu',input_shape=(train_data.shape[1],)));
    model.add(layers.Dense(64,activation='relu'));
    model.add(layers.Dense(1));
    '''
    编译网络用的是 mse 损失函数，即均方误差（MSE，mean squared error），预测值与
目标值之差的平方。这是回归问题常用的损失函数。
在训练过程中还监控一个新指标：平均绝对误差（MAE，mean absolute error）。它是预测值
与目标值之差的绝对值。比如，如果这个问题的 MAE 等于 0.5，就表示你预测的房价与实际价
格平均相差 500 美元。
    '''
    model.compile(optimizer='rmsprop',loss='mse',metrics=['mae'])
    return model;

def KFoldCrossValidation(train_data, train_targets):
    """
    使用 K 折交叉验证模型
    为了在调节网络参数（比如训练的轮数）的同时对网络进行评估，可以将数据划分为训练集和验证集。
    但由于数据点很少，验证集会非常小（比如大约100 个样本）。因此，验证分数可能会有很大波动，这取决于你所选择的验证集和训练集。
    也就是说，验证集的划分方式可能会造成验证分数上有很大的方差，这样就无法对模型进行可靠的评估。在这种情况下，最佳做法是使用 K 折交叉验证
    这种方法将可用数据划分为 K个分区（K 通常取 4 或 5），实例化 K 个相同的模型，将每个模型在 K-1 个分区上训练，
    并在剩下的一个分区上进行评估。模型的验证分数等于 K 个验证分数的平均值。
    :param train_data: 训练特征集
    :param train_targets:训练结果集
    :return:
    """
    k =4;
    num_val_samples = len(train_data)//k;
    num_epochs = 500;
    all_mae_histories = [];
    for i in range(k):
        print('processing flod #',i);
        # 准备验证数据：第k个分区的数据
        val_data = train_data[i * num_val_samples:(i+1)*num_val_samples]
        val_targets = train_targets[i * num_val_samples:(i+1)*num_val_samples];
        # 准备训练数据：其他所有分区的数据
        partial_train_data = np.concatenate(
            [train_data[:i * num_val_samples],
             train_data[(i+1) * num_val_samples:]],
            axis=0)# 是numpy中对array进行拼接的函数 ，将K折划分的训练集进行拼接，axis=0则代表着按照第一维度进行拼接
        partial_train_targets = np.concatenate(
            [train_targets[:i * num_val_samples],
             train_targets[(i + 1) * num_val_samples:]],
            axis=0)
        model = modelCreat(train_data);
        # 训练模式（静默模式，verbose=0）validation_data用来在每个epoch之后，或者每几个epoch，验证一次验证集，用来及早发现问题
        history = model.fit(partial_train_data, partial_train_targets,
                  validation_data=(val_data,val_targets),
                  epochs=num_epochs, batch_size=2048, verbose=0)
        # 在验证数据上评估模型
        maw_history = history.history['val_mae']# 获取测试集的平均绝对误差
        all_mae_histories.append(maw_history)
    print(all_mae_histories)
    # 计算所有轮次中的 K 折验证分数平均值
    average_mae_history = [
        np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)
    ]
    return average_mae_history;



def smooth_curve(points,factor=0.9):
    """
    删除指定个数数据点
    :param points:
    :param factor:
    :return:
    """
    smoothed_points = [];
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1];
            smoothed_points.append(previous *factor +point *(1-factor));
        else:
            smoothed_points.append(point)
    return smoothed_points;

if __name__=="__main__":
    (train_data, train_targets), (test_data, test_targets) = getBostonData();
    train_data,test_data = standardization(train_data,test_data);
    print(train_data)
    average_mae_history = KFoldCrossValidation(train_data, train_targets);

    smooth_mae_history = smooth_curve(average_mae_history[200:]);
    mtp.mappingMAE(smooth_mae_history);