# -*- coding: utf-8 -*-
# @Time : 2021/2/18 11:09
# @Author : Zhining Zhang
# @site :  
# @File : cat_dog_fit.py
# @main : 使用fit实现猫狗分类（需要超大内存）
# @Software: PyCharm
from PIL import Image
import numpy as np
import os
import time
from keras import layers
from keras import models
from keras import optimizers
import Dense_all_link.mapping_training_process as  mtp
# import tensorflow as tf
# tf.compat.v1.disable_eager_execution()
def getImageData(path):
    pil_img = Image.open(path)
    pil_img = pil_img.resize((150,150),Image.ANTIALIAS)
    img = np.array(pil_img)
    return img/255;
def getData():
    image_doge = []
    image_doge_lable=[];
    image_cat = [];
    image_cat_lable=[];
    path_main = "D:\\贵州大学\\数据集\\dogs-vs-cats\\newTrain\\train"
    img_file_list = os.listdir(path_main)
    for i in img_file_list:
        if('dog' in i):
            if(len(image_doge)>=1000):
                continue
            image_doge.append(getImageData(path_main+"\\"+i).tolist())
            image_doge_lable.append(1)
        else:
            if(len(image_cat)>=1000):
                continue
            image_cat.append(getImageData(path_main+"\\"+i).tolist())
            image_cat_lable.append(0)
    image_doge = getSlipTrain(image_doge)
    image_doge_lable = getSlipTrain(image_doge_lable)
    image_cat = getSlipTrain(image_cat)
    image_cat_lable = getSlipTrain(image_cat_lable)
    return (np.array(image_doge[0]+image_cat[0]),np.array(image_doge_lable[0]+image_cat_lable[0])),\
           (np.array(image_doge[1]+image_cat[1]),np.array(image_doge_lable[1]+image_cat_lable[1])),\
           (np.array(image_doge[2]+image_cat[2]),np.array(image_doge_lable[2]+image_cat_lable[2]))
def getSlipTrain(list_name):
    length = len(list_name);
    end1 = int(length * 6 / 10);
    end2 = end1 + int(length * 2 / 10);
    return list_name[:end1],list_name[end1:end2],list_name[end2:]

def modelCreate(x_train,y_train,x_test, y_test):
    print(type(x_test))
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(150, 150, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    print(model.summary())
    model.compile(loss='binary_crossentropy',
        optimizer=optimizers.RMSprop(lr=1e-4),
        metrics=['acc'])
    history = model.fit(
        x_train, y_train,
        epochs=20,
        batch_size=1,
        validation_data=(x_test, y_test))

    print(history)
    return history.history
if __name__=="__main__":
    start_time = time.time();
    (test_train,test_lable),(test1_train,test1_lable),(end_train,end_lable)=getData();
    history_dict = modelCreate(test_train,test_lable,test1_train,test1_lable)
    end_time = time.time();
    mtp.mappingLoss(history_dict)
    mtp.mappingAcc(history_dict)

    end_time = time.time();
    print(end_time-start_time)
