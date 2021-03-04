#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/4 15:42
# @Author : Aries
# @Site : 猫狗分类使用vgg16，并对卷积层进行解冻微调
# @File : cat_dog_vgg16_trim.py
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
    #trainable为False的变量仅代表在训练过程中无需保存与更新梯度等操作，要微调必须设置为True
    conv_base.trainable = True
    # 对后三层进行解冻
    set_trainable = False
    for layer in conv_base.layers:#修改VGG16的值
        if layer.name == 'block5_conv1':
            set_trainable=True
        if set_trainable:
            layer.trainable = True
        else:
            layer.trainable = False
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    # 我们将使用学习率非常小的 RMSProp 优化器来实现。之所以让
    # 学习率很小，是因为对于微调的三层表示，我们希望其变化范围不要太大。太大的权重更新可
    # 能会破坏这些表示。
    model.compile(loss='binary_crossentropy',
                 optimizer=optimizers.RMSprop(lr=1e-5),
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
