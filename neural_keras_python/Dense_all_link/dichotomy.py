# -*- coding: utf-8 -*-
# @Time : 2021/1/14 13:39
# @Author : Zhining Zhang
# @site :  
# @File : dichotomy.py
# @main : 二分类问题，以电影评论为例
# @Software: PyCharm

from keras.datasets import imdb
import numpy as np;
from keras import models;
from keras import layers;
from Dense_all_link import mapping_training_process as mtp

def getImdbData():
    '''
    加载IMDB数据，IMDB已经对数据进行预处理了，已经将评论中的单词转换为整数了即{'gussied': 65111, "bullock's": 32066, "'delivery'": 65112,....}
    :return:
    '''
    # 获取训练数据前10000个最常出现的单词，低频单词将被舍弃,
    # train_data[0]=[1,14,22,16,...]这些数字表示单词的索引，train_labels=[1 0 0 ... 0 1 0],1代表正面评论，0代表负面评论
    (train_data,train_labels),(test_data,test_labels) = imdb.load_data(num_words=10000)
    # # 将数字序列解码为单词
    # word_index = imdb.get_word_index();
    # reverse_word_index = dict(
    #     [(value,key) for (key,value) in word_index.items()]
    # )
    # decoded_review = ' '.join(
    #     #将评论解码时索引要减去3，因为0、1、2是为padding、start of sequence和unknown这三个词保留的索引，当索引-3<=0时输出？表示这一条评论结束下一条开始
    #     [reverse_word_index.get(i-3,'?') for i in train_data[0]]
    # )
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
    '''什么是激活函数？为什么要使用激活函数？
        如果没有 relu 等激活函数（也叫非线性），Dense 层将只包含两个线性运算——点积和加法：
        output = dot(W, input) + b
        这样 Dense 层就只能学习输入数据的线性变换（仿射变换）：该层的假设空间是从输
        入数据到 16 位空间所有可能的线性变换集合。这种假设空间非常有限，无法利用多个表示
        层的优势，因为多个线性层堆叠实现的仍是线性运算，添加层数并不会扩展假设空间。
        为了得到更丰富的假设空间，从而充分利用多层表示的优势，你需要添加非线性或激
        活函数。relu 是深度学习中最常用的激活函数，但还有许多其他函数可选，它们都有类似
        的奇怪名称，比如 prelu、elu 等。'''
    model.add(layers.Dense(16,activation='relu',input_shape=(10000,)));#传入该层隐藏单元是16个，激活函数是relu，输入的样本最大轴是10000
    model.add(layers.Dense(16,activation='relu'));# 传入该层隐藏单元是16个，激活函数是relu
    model.add(layers.Dense(1,activation='sigmoid'));# 传入该层隐藏单元是1个，激活函数是sigmoid
    # 编译模型由于是二分类问题所有使用二元交叉熵损失函数binary_crossentropy，也可以使用均方误差squared_error
    model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['accuracy']);
    # 训练模型
    history = model.fit(x_train,y_train,epochs=20,batch_size=2048,validation_data=(x_test,y_test))
    #获取训练过程和验证过程总监控的指标
    ''' loss：训练集损失值
        accuracy:训练集准确率
        val_loss:测试集损失值
        val_accruacy:测试集准确率'''
    history_dict = history.history;
    print(history_dict.keys())# dict_keys(['loss', 'accuracy', 'val_loss', 'val_accuracy'])
    print(model.evaluate(x_test,y_test))# 返回的是 损失值和你选定的指标值
    return history_dict;



if __name__=="__main__":
    (train_data, train_labels), (test_data, test_labels) = getImdbData();
    x_train = vectorize_sequences(train_data)
    x_test = vectorize_sequences(test_data)
    y_train = np.asarray(train_labels).astype('float32')# 将list转为张量
    y_test = np.asarray(test_labels).astype('float32')
    history_dict = modelCreat(x_train,y_train,x_test,y_test)
    mtp.mappingLoss(history_dict)
    mtp.mappingAcc(history_dict)