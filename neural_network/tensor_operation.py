# -*- coding: utf-8 -*-
# @Time : 2020/11/26 9:47
# @Author : Zhining Zhang
# @site :  
# @File : tensor_operation.py
# @main : 张量运算
# @Software: PyCharm
import numpy as np;
# 随机生成1个4维的张量，2个样本，样本的高度是3，宽度是2，通道数是4
x = np.random.random((2,3,2,4));
print("这是x\n:{}".format(x))
# 随机生成1个
y = np.random.random((2,1));
print("这是y\n:{}".format(y))
z = np.maximum(x,y);
