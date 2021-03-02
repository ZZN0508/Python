# -*- coding: utf-8 -*-
# @Time : 2021/1/13 10:43
# @Author : Zhining Zhang
# @site :  
# @File : test.py
# @main : 
# @Software: PyCharm
# K折验证
# 导入数据集
import skimage.io as io
import os, sys
from skimage import data_dir
import numpy as np
import matplotlib.pyplot as plt
import cv2

from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

datagen = ImageDataGenerator(rotation_range=40,  # 随机旋转角度的范围
                             width_shift_range=0.2,  # 随机转换图片宽度的范围
                             height_shift_range=0.2,  # 随机转换图片高度的范围
                             shear_range=0.2,  # 随机剪切转换比例
                             zoom_range=0.2,  # 随机放缩比例
                             horizontal_flip=True,  # 开启水平翻转
                             fill_mode='nearest'  # 填充策略
                             )

path = "D:/贵州大学/数据集/dogs-vs-cats/newTrain/train/";
dirs = os.listdir(path)
# 保存本地
# for file in dirs:
#     img = load_img(path+file)
#     x = img_to_array(img)
#     x = x.reshape((1,) + x.shape)  # 这是一个numpy数组，形状为 (1,150, 150,3)
#     i = 0
#     for batch in datagen.flow(x, batch_size=1,
#                           save_to_dir='/data_2/everyday/0312/others/pic-aug'):
#        i += 1
#        if i > 50:             # 数据扩充倍数，此处为数据扩充50倍
#         break             #  否则生成器会退出循环


for file in dirs[:3]:
    img = load_img(path + file)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)  # 这是一个numpy数组，形状为 (1,150, 150,3)
    i = 0
    for batch in datagen.flow(x, batch_size=1):
        # cv2.imshow("src",x[0][:,:,::-1])
        # cv2.waitKey(0)
        plt.figure(i)
        imgplot = plt.imshow(array_to_img(batch[0]))
        plt.show()
        i += 1
        if 0 == i % 10:
            break
