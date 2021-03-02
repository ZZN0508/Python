# -*- coding: utf-8 -*-
# @Time : 2020/11/26 14:49
# @Author : Zhining Zhang
# @site :  
# @File : Keras_line.py
# @main : 线性回归
# @Software: PyCharm
import numpy as np

np.random.seed(1337)
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

# 生成数据
X = np.linspace(-1, 1, 200)  # 在返回（-1, 1）范围内的等差序列
np.random.shuffle(X)  # 打乱顺序
Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200,))  # 生成Y并添加噪声
# plot
plt.scatter(X, Y)
plt.show()

X_train, Y_train = X[:160], Y[:160]  # 前160组数据为训练数据集
X_test, Y_test = X[160:], Y[160:]  # 后40组数据为测试数据集

# 构建神经网络模型
model = Sequential()
#input_dim数据输入状态就是几个自变量;units:该层有几个神经元即函数未知参数有几个;activation:该层使用的激活函数;use_bias:是否添加偏置项;kernel_initializer:权重初始化方法
#bias_initializer:偏置值初始化方法;kernel_regularizer:权重规范化函数;bias_regularizer:偏置值规范化方法
#activity_regularizer:输出的规范化方法;kernel_constraint:权重变化限制函数;bias_constraint:偏置值变化限制函数
model.add(Dense(input_dim=1,units=1))
# model.add(Dense(input_dim=1, units=1))

# 选定loss函数和优化器，进行训练
model.compile(loss='mse', optimizer='sgd')

# 开始训练
print('Training -----------')
# for step in range(501):
#     cost = model.train_on_batch(X_train, Y_train);# Keras有很多开始训练的函数，这里用train_on_batch（）
#     if step % 50 == 0:
#         print("After %d trainings, the cost: %f" % (step, cost))
'''keras中的三中模型训练 fit(),fit_generator(),train_on_batch()
fit:我们的网络将在原始数据上训练。原始数据本身将适合内存，我们无需将旧批量数据从RAM中移出并将新批量数据移入RAM。
    此外，我们不会使用数据增强动态操纵(在现有的数据集中进行增加，如只有一张图，我们可以对图片旋转，剪切来增加数据量)训练数据
    对于小型，简单化的数据集，使用Keras的.fit函数是完全可以接受的。
    训练模型，model.fit(训练图像,训练图像对应的标签,所有的样本训练5次,样本每次拿128个进行训练);
    model.fit(train_images,one_hot_train_labels,epochs=5,batch_size=128);
fit_generator:函数假定存在一个为其生成数据的基础函数。
        aug是一个Keras ImageDataGenerator对象，用于图像的数据增强，随机平移，旋转，调整大小等。epochs设置样本训练次数，执行数据增强是正则化的一种形式，使我们的模型能够更好的被泛化。
    但是，应用数据增强意味着我们的训练数据不再是“静态的” ——数据不断变化。根据提供给ImageDataGenerator的参数随机调整每批新数据。Keras数据生成器意味着无限循环，它永远不会返回或退出。
        .fit_generator时提供steps_per_epoch参数（.fit方法没有这样的参数）。是由于该函数旨在无限循环，因此Keras无法确定一个epoch何时开始的，并且新的epoch何时开始。
    因此，我们将训练数据的总数除以批量大小的结果作为steps_per_epoch的值。一旦Keras到达这一步，它就会知道这是一个新的epoch。
    model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS)
train_on_batch:函数接受单批数据，执行反向传播，然后更新模型参数。该批数据可以是任意大小的（即，它不需要提供明确的批量大小）。您也可以生成数据。
    此数据可以是磁盘上的原始图像，也可以是以某种方式修改或扩充的数据。
    当您有非常明确的理由想要维护自己的训练数据迭代器时，通常会使用.train_on_batch函数，例如数据迭代过程非常复杂并且需要自定义代码。	
    '''
his=model.fit(X_train, Y_train, epochs=500, batch_size=512)

# 测试过程
print('\nTesting ------------')
cost = model.evaluate(X_test, Y_test, batch_size=500)
print('test cost:', cost)
# 查看训练出的网络参数
# 由于我们网络只有一层，且每次训练的输入只有一个，输出只有一个
# 因此第一层训练出Y=WX+B这个模型，其中W,b为训练出的参数
W,b=model.layers[0].get_weights()
print('Weights=', W, '\nbiases=', b)

# 将训练结果绘出
Y_pred = model.predict(X_test)
plt.scatter(X_test, Y_test)
plt.plot(X_test, Y_pred)

plt.show()