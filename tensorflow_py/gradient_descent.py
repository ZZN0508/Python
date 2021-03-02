# -*- coding: utf-8 -*-
# @Time : 2020/11/16 9:09
# @Author : Zhining Zhang
# @site :  
# @File : gradient_descent.py
# @main : 使用tensorflow实现梯度下降算法
# @Software: PyCharm
import tensorflow as tf
import matplotlib.pyplot as plt
import math
import numpy as np;

# 说明使用tensorflow1.0版本
tf.compat.v1.disable_eager_execution()
tf1_x=tf.compat.v1;
# 产生一个长度为15的一维张量
x=tf1_x.Variable(15.0, dtype=tf.float32)
# 构造函数y=(x-1)^2
y=tf1_x.pow(x-1, 2.0)
# 调用梯度下降优化函数
learning_rate = tf1_x.placeholder(tf.float32, shape=[])
opti=tf1_x.train. GradientDescentOptimizer(learning_rate=learning_rate).minimize(y)
# 画函数曲线
value=np.arange(-15,17,0.01)
y_value=np.power(value-1, 2.0)
plt.plot(value,y_value)
# 创建会话
session=tf1_x.Session()
# 添加节点用于初始化所有的变量
session.run(tf1_x.global_variables_initializer())
value_learng_list=[]
for i in range(50):
   value_learng_list.append(round((i+1)*3*0.001, 3))
print(value_learng_list)
#”迭代
for i in range(200):
   session.run(opti,feed_dict={learning_rate: 0.01/(i+1)})
   v=session.run(x)
   plt.plot(v, math. pow(v-1, 2.0),'go')
   print('第%d次的x的迭代值:%f'%(i+1,v))
plt.show()


