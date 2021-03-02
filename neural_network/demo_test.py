# -*- coding: utf-8 -*-
# @Time : 2020/11/24 9:25
# @Author : Zhining Zhang
# @site :  
# @File : demo_test.py
# @main : 一个测试内容
# @Software: PyCharm
from keras import layers
from keras import models
from keras.datasets import mnist
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
def demo():
    # 定义一个神将网络层
    model = models.Sequential();
    # 输入的是784为特征，没有样本，样本为任意，输出为32，这是二维张量
    layer = layers.Dense(32, input_shape=(784,));
    # 模型添加第一次层
    model.add(layer)
    # 模型添加第二个层
    # layers.Dense(16)输出是16，没有输入，但是输入会自动使用上一层的输出32
    model.add(layers.Dense(16))
    print(layer);
def mnist_test():
    #(真是图像,真实图像对应的值),(测试图像,测试图像对应的值) = mnist训练集;
    (train_images,train_labels),(test_images,test_labels) = mnist.load_data();

    # train_images数组原来含有60000个元素，每个元素是一个28行，28列的二维数组，
    # 现在把每个二维数组转变为一个含有28*28个元素的一维数组。
    train_images = train_images.reshape(60000,28*28);
    test_images = test_images.reshape(10000,28*28);

    #由于数字图案是一个灰度图，图片中每个像素点值的大小范围在0到255之间，
    # 代码把每个像素点的值从范围0-255转变为范围在0-1之间的浮点值。
    train_images = train_images.astype('float32') / 255;
    test_images = test_images.astype('float32') / 255;

    #接着我们把图片对应的标记也做一个更该，目前所有图片的数字图案对应的是0到9，
    # 例如test_images[0]对应的是数字7的手写图案，那么其对应的标记test_labels[0]的值就是7，
    # 我们需要把数值7变成一个含有10个元素的数组，然后在低7个元素设置为1，
    # 其他元素设置为0，例如test_lables[0] 的值由7转变为数组[0,0,0,0,0,0,0,1,0,0,],
    one_hot_train_labels = to_categorical(train_labels);
    one_hot_test_labels = to_categorical(test_labels);

    # 创建训练模型
    #表示我们要把每一个数据处理层串联起来，就好像用一根线把一排珠子串起来一样。
    # 神经网络的数据处理层之间的组合方式有多种，串联是其中一种，也是最常用的一种。
    model = models.Sequential();
    # 构建第一层模型
    #构造一个Dense层全连接层,接受数据格式为28*28的二维数组，
    # 后面的“,“表示数组里面的每一个元素到底包含多少个数字都没有关系
    #激活函数使用relu，输出是512个
    model.add(layers.Dense(units=512,activation='relu',input_shape=(28*28,)))
    # 构建第二层模型
    # 输出是10，没有输入，但是输入会自动使用上一层的输出32，激活函数实现softmax
    model.add(layers.Dense(units=10,activation='softmax'))
    # model.compile()用于在配置训练方法时，告知训练时用的优化器、损失函数和准确率评测标准
    #损失函数使用categorical_crossentropy,优化器使用rmsprop,准确率使用accuracy
    #返回训练中的损失函数(history.history.loss)和准确率(history.history.accuracy)
    history = model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

    #训练模型，model.fit(训练图像,训练图像对应的标签,所有的样本训练5次,样本每次拿128个进行训练);
    model.fit(train_images,one_hot_train_labels,epochs=5,batch_size=128);

    # 使用测试时间测试模型
    test_loss,test_acc = model.evaluate(test_images,one_hot_test_labels)
    print('test_loss={}'.format(test_loss))
    print('test_acc={}'.format(test_acc))

    #预测
    predictions = model.predict(test_images);

    print('输入参数 : 预测值 : 真实值');
    #zip() 函数是 Python 内置函数之一，它可以将多个序列（列表、元组、字典、集合、字符串以及 range() 区间构成的列表）“压缩”成一个 zip 对象。所谓“压缩”，其实就是将这些序列中对应位置的元素重新组合，生成一个个新的元组。
    train_value=[]
    thure_value=[];
    test_value=[]
    for train,predic,actual in zip(train_images,predictions,test_labels):
        print('{} : {} : {}'.format(np.argmax(train),np.argmax(predic),actual));
        thure_value.append(np.argmax(predic));
        test_value.append(actual);
        train_value.append(np.argmax(train));
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(np.array(train_value), np.array(thure_value), s=30, c='red', marker='s')
    ax.scatter(np.array(train_value), np.array(test_value), s=30, c='green')
    plt.show()

if __name__=="__main__":
    mnist_test();