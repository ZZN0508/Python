# -*- coding: utf-8 -*-
# @Time : 2021/2/8 10:26
# @Author : Zhining Zhang
# @site :
# @File : cat_dog_vgg16.py
# @main : 猫狗分类使用VGG16卷积不使用数据增强的快速特征提取
# @Software: PyCharm
from keras.applications import VGG16
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras import layers
from keras import optimizers
import time
import Dense_all_link.mapping_training_process as  mtp
'''
这里向构造函数中传入了三个参数。
 weights 指定模型初始化的权重检查点。
 include_top 指定模型最后是否包含密集连接分类器。默认情况下，这个密集连接分类器对应于 ImageNet 的 1000 个类别。
 input_shape 是输入到网络中的图像张量的形状。这个参数完全是可选的，如果不传入这个参数，那么网络能够处理任意形状的输入。
'''
conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(150, 150, 3))
print(conv_base.summary())


def extract_features(directory,sample_count):
    """
    特征提取，提取特征形象（samples,4,4,512) 图片大小4x4颜色通道512
    因为VGG16模型输出的数据是（4，4，512）结构的，所以先创建一个结构为（样本数，4，4，512）的全零矩阵和一个行数为样本数的标签矩阵。
    下面将每个批次的输出结果（通过conv_pridect()）写到特征矩阵中等待接下来的输入全连接层处理。
    :param directory: 图片位置
    :param sample_count: 样本数
    :return:卷积基提取后的特征
    """
    batch_size = 20
    datagen = ImageDataGenerator(rescale=1. / 255)
    features = np.zeros(shape=(sample_count,4,4,512))
    labels = np.zeros(shape=(sample_count))
    generator = datagen.flow_from_directory(
       directory,
       target_size=(150,150),
       batch_size=batch_size,
       class_mode='binary'
    )
    i=0
    for inputs_batch, labels_batch in generator:
        features_batch = conv_base.predict(inputs_batch)# 使用VGG16模型的特征提取
        features[i * batch_size : (i+1) * batch_size] = features_batch;
        labels[i * batch_size : (i+1) * batch_size] = labels_batch
        i+=1
        if i * batch_size >=sample_count:
            break
    features = np.reshape(features, (sample_count, 4 * 4 * 512))
    return features,labels

def modelCreat(train_features,train_labels,validation_features,validation_labels):
    model = models.Sequential()
    model.add(layers.Dense(256,activation='relu',input_dim=4*4*512))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1,activation='sigmoid'))
    model.compile(optimizer=optimizers.RMSprop(lr=2e-5),
                  loss='binary_crossentropy',
                  metrics=['acc'])
    history = model.fit(train_features,train_labels,
                        epochs=30,
                        batch_size=20,
                        validation_data=(validation_features,validation_labels))
    return history.history;

if __name__=="__main__":
    start_time = time.time();
    train_features, train_labels = extract_features(r'D:\贵州大学\数据集\dogs-vs-cats\train\train', 2000)
    validation_features, validation_labels = extract_features(r'D:\贵州大学\数据集\dogs-vs-cats\train\test', 1000)
    test_features, test_labels = extract_features(r'D:\贵州大学\数据集\dogs-vs-cats\train\test1', 1000)
    history_dict = modelCreat(train_features,train_labels,validation_features,validation_labels)
    end_time = time.time();
    mtp.mappingLoss(history_dict)
    mtp.mappingAcc(history_dict)
    print(end_time - start_time)
