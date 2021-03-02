# -*- coding: utf-8 -*-
# @Time : 2021/1/30 10:16
# @Author : Zhining Zhang
# @site :  
# @File : handwritten_num_recognition.py
# @main : 
# @Software: PyCharm
from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical
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
    train_images = train_images.reshape((len(train_labels), 28 * 28))
    train_images = train_images.astype('float32') / 255

    test_images = test_images.reshape((len(test_labels), 28 * 28))
    test_images = test_images.astype('float32') / 255

    #将标签类型转换为二进制编码数据
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    return (train_images, train_labels), (test_images, test_labels);


def modelCreat(train_images, train_labels,test_images, test_labels):
    """
    神经网络构建：
    网络包含 2 个 Dense 层，它们是密集连接（也叫全连接）的神经层。第二层（也
    是最后一层）是一个 10 路 softmax 层，它将返回一个由 10 个概率值（总和为 1）组成的数组。
    每个概率值表示当前数字图像属于 10 个数字类别中某一个的概率
    """
    model = models.Sequential()
    model.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=5, batch_size=1024)
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('test_loss:', test_loss)
    print('test_acc:', test_acc)

if __name__=="__main__":
    (train_images, train_labels), (test_images, test_labels)=getDateMNIST();
    modelCreat(train_images, train_labels,test_images, test_labels)