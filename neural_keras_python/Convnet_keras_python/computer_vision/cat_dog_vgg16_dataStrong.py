#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/3 21:02
# @Author : Aries
# @Site : 猫狗分类使用VGG16卷积使用数据增强的快速特征提取
# @File : cat_dog_vgg16_dataStrong.py
# @Software: PyCharm
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras import models
from keras import layers
from keras.applications import VGG16
import time
import Dense_all_link.mapping_training_process as  mtp
def readImage():
    # 进行图像预处理
    '''
     rescale进行图像预处理，将所有图像乘以 1/255 缩放
    :return:
    '''
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    # 转为张量
    train_generator = train_datagen.flow_from_directory(
        'D:\\贵州大学\\数据集\\dogs-vs-cats\\train\\test',
        target_size=(150,150),#将所有图像的大小调整为 150×150
        batch_size=20,
        class_mode='binary'#因为使用了 binary_crossentropy损失，所以需要用二进制标签
    )

    validation_generator = test_datagen.flow_from_directory(
        'D:\\贵州大学\\数据集\\dogs-vs-cats\\train\\test1',
        target_size=(150, 150),  # 将所有图像的大小调整为 150×150
        batch_size=20,
        class_mode='binary'  # 因为使用了 binary_crossentropy损失，所以需要用二进制标签
    )
    print(validation_generator)
    return train_generator,validation_generator

def modelCreate(train_generator,validation_generator):
    conv_base = VGG16(weights='imagenet',
                      include_top=False,
                      input_shape=(150, 150, 3))
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                 optimizer=optimizers.RMSprop(lr=2e-5),
                 metrics=['acc'])
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=100,
        epochs=30,
        validation_data=validation_generator,
        validation_steps=50)
    return history.history

if __name__=="__main__":
    start_time = time.time();
    train_generator,validation_generator = readImage();
    history_dict = modelCreate(train_generator,validation_generator)
    end_time = time.time();
    mtp.mappingLoss(history_dict)
    mtp.mappingAcc(history_dict)
    print(end_time-start_time)
