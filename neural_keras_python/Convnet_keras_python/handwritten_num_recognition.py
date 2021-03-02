# -*- coding: utf-8 -*-
# @Time : 2021/1/30 10:36
# @Author : Zhining Zhang
# @site :  
# @File : handwritten_num_recognition.py
# @main : 
# @Software: PyCharm
from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical
import time
def getDateMNIST():
    """
    数据处理：
        将手写数字的灰度图像（28 像素×28 像素）划分到 10 个类别中（0~9）。
        我们将使用 MNIST 数据集，这个数据集包含 60 000 张训练图像和 10 000 张测试图像

        对数据进行预处理，将其变换为网络要求的形状，并缩放到所有值都在 [0, 1] 区间。
        比如，之前训练图像保存在一个 uint8 类型的数组中，其形状为(60000, 28, 28) ，取值区间为 [0, 255] 。
        我们需要将其变换为一个 float32 数组，其形状为 (60000, 28 * 28) ，取值范围为 0~1。

        将标签类型转换为二进制编码数据
    :return: 预处理后测试集和训练集
    """
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data();

    # 数据进行预处理
    train_images = train_images.reshape((len(train_labels), 28,28,1))
    train_images = train_images.astype('float32') / 255

    test_images = test_images.reshape((len(test_labels), 28 , 28 ,1))
    test_images = test_images.astype('float32') / 255

    #将标签类型转换为二进制编码数据
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)
    print(type(train_images))
    print(train_images)
    return (train_images, train_labels), (test_images, test_labels);


def modelCreat(train_images, train_labels,test_images, test_labels):
    """
    神经网络构建：
    卷积神经网络接收形状为 (image_height, image_width, image_channels)的输入张量（不包括批量维度）。
    本例中设置卷积神经网络处理大小为 (28, 28, 1) 的输入张量，这正是 MNIST 图像的格式。
    我们向第一层传入参数 input_shape=(28, 28, 1) 来完成此设置。

    第一个卷积层接收一个大小为 (28, 28, 1) 的特征图，并输出一个大小为 (26, 26, 32) 的特征图，即它在输入上计算 32 个过滤器。
    对于这 32 个输出通道，每个通道都包含一个 26×26 的数值网格，它是过滤器对输入的响应图（response map）， 表示这个过滤器模式在输入中不同位置的响应。

    从输入中提取的图块尺寸：这些图块的大小通常是 3×3 或 5×5。本例中为 3×3，这是很常见的选择。
    输出特征图的深度：卷积所计算的过滤器的数量。本例第一层的深度为 32，最后一层的深度是 64
    """
    #卷积神经网络
    model = models.Sequential()
    model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)));
    model.add(layers.MaxPooling2D(2,2));
    model.add(layers.Conv2D(64, (3, 3), activation='relu'));
    model.add(layers.MaxPooling2D(2, 2));
    model.add(layers.Conv2D(64, (3, 3), activation='relu'));
    print(model.summary())

    #全连接
    model.add(layers.Flatten())#Flatten层用来将输入“压平”，即把多维的输入一维化，常用在从卷积层到全连接层的过渡。
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    print(model.summary())

    model.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=5, batch_size=1024)
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('test_loss:', test_loss)
    print('test_acc:', test_acc)

def maxPoolModel():
    model_no_max_pool = models.Sequential();
    model_no_max_pool.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)));
    model_no_max_pool.add(layers.Conv2D(64,(3,3),activation='relu'))
    model_no_max_pool.add(layers.Conv2D(64,(3,3),activation='relu'))
    print(model_no_max_pool.summary())
if __name__=="__main__":
    start_time = time.time();
    maxPoolModel()

    (train_images, train_labels), (test_images, test_labels)=getDateMNIST();
    # modelCreat(train_images, train_labels,test_images, test_labels)
    print("总时间{0}".format(time.time() - start_time))