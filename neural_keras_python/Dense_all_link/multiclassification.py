# -*- coding: utf-8 -*-
# @Time : 2021/1/15 19:43
# @Author : Zhining Zhang
# @site :  
# @File : multiclassification.py
# @main : 多分类问题-新闻分类
# @Software: PyCharm
import numpy as np;
from keras.utils.np_utils import to_categorical;
from keras import models;
from keras import layers;
from Dense_all_link import mapping_training_process as mtp
from keras.datasets import reuters

def getMnistData():
    (train_data, train_labels), (test_data, test_labels) = reuters.load_data(
        num_words=10000)
    return (train_data,train_labels),(test_data,test_labels);

def vectorize_sequences(sequences,dimension=10000):
    '''
    将整数序列编码为二进制矩阵
    如sequences=[1,3,4,2],dimension=5
    results=[[0. 0. 0. 0. 0.][0. 0. 0. 0. 0.][0. 0. 0. 0. 0.][0. 0. 0. 0. 0.]]
    results=[[0. 1. 0. 0. 0.][0. 0. 0. 1. 0.][0. 0. 0. 0. 1.][0. 0. 1. 0. 0.]]
    :param sequences:待转换的数据
    :param dimension:数据索引最大值
    :return:转换后的矩阵
    '''
    results = np.zeros((len(sequences),dimension));# 生成一个2D张量，
    for i ,sequence in enumerate(sequences):
        results[i,sequence] = 1;# 将results[i]设置为1
    return results;

def modelCreat(x_train,y_train,x_test,y_test):
    """
    模型定义
    :param x_train:训练数据X
    :param y_train：训练数据y
    :param x_test:测试数据X
    :param y_test：测试数据y
    """
    model = models.Sequential();
    # 要中间层维度足够大，如果中间层远远小于输入的维度，那么会造成信息瓶颈，导致精度下降
    model.add(layers.Dense(128,activation='relu',input_shape=(10000,)));#传入该层隐藏单元是16个，激活函数是relu，输入的样本最大轴是10000
    model.add(layers.Dense(128,activation='relu'));# 传入该层隐藏单元是16个，激活函数是relu
    model.add(layers.Dense(128, activation='relu'));  # 传入该层隐藏单元是16个，激活函数是relu
    model.add(layers.Dense(46,activation='sigmoid'));# 传入该层隐藏单元是1个，激活函数是sigmoid
    # 编译模型由于是多分类问题所有使用分类交叉熵损失函数categorical_crossentropy，也可以使用均方误差squared_error
    # 标签遵循分类编号使用categorical_crossentropy，如果遵循整数标签则准询sparse_categorical_crossentropy
    # 标签遵循分类编号 就是使用to_categorical(test_labels),整数标签是np.array(test_labels)
    model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy']);
    # 训练模型
    history = model.fit(x_train,y_train,epochs=20,batch_size=2048,validation_data=(x_test,y_test))
    print(history)
    #获取训练过程和验证过程总监控的指标
    ''' loss：训练集损失值
        accuracy:训练集准确率
        val_loss:测试集损失值
        val_accruacy:测试集准确率'''
    history_dict = history.history;
    print(history_dict.keys())# dict_keys(['loss', 'accuracy', 'val_loss', 'val_accuracy'])
    print(model.evaluate(x_test,y_test))# 返回的是 损失值和你选定的指标值
    predictions = model.predict(x_test);# 返回值是数值，表示样本属于每一个类别的概率
    print(predictions[0].shape)# (46,)表示predictions中元素长度都是46的2D张量
    print(format(np.sum(predictions[0]),'.5f'))# 为1，因为所有概率的和为1
    print(np.argmax(predictions[0]))# 返回概率最大的类别
    return history_dict;


if __name__=="__main__":
    (train_data,train_labels),(test_data,test_labels) = getMnistData();
    x_train = vectorize_sequences(train_data)
    x_test = vectorize_sequences(test_data)
    #to_categorical()和vectorize_sequences()类似，只是to_categorical要求数据列表长度是一样的
    #如[[1,2,3],[2,3,4]]是可以的，但是[[1,2,3],[2,4]]不行，因为第一个长度是3第二个是2
    y_train = to_categorical(train_labels)  #将标签类型转换为二进制编码数据
    y_test = to_categorical(test_labels)
    history_dict = modelCreat(x_train, y_train, x_test, y_test)
    mtp.mappingLoss(history_dict)
    mtp.mappingAcc(history_dict)


