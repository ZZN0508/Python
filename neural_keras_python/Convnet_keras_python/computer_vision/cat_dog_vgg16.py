# -*- coding: utf-8 -*-
# @Time : 2021/2/8 10:26
# @Author : Zhining Zhang
# @site :
# @File : cat_dog.py
# @main : 猫狗分类使用VGG16卷积
# @Software: PyCharm
from keras.applications import VGG16
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
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

def getData():
    base_dir = ''