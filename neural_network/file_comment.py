# -*- coding: utf-8 -*-
# @Time : 2020/11/26 11:12
# @Author : Zhining Zhang
# @site :  
# @File : file_comment.py
# @main : 电影评论分类
# @Software: PyCharm
from keras.datasets import imdb as db
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics
import numpy as np
import matplotlib.pyplot as plt

# 矢量序列化
def build_model():
    model = models.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 画矢量图
def draw(history):
    """
    :param history:
    :return:
    """
    history_dict = history.history
    types = filter(lambda i: '_' not in i, history_dict.keys())
    for type in types:
        values = history_dict[type]
        validate_values = history_dict['val_{}'.format(type)]
        epochs = range(1, len(values) + 1)
        # plt.clf()
        plt.plot(epochs, values, 'bo', label='Training {}'.format(type))
        plt.plot(epochs, validate_values, 'b', label='Validation {}'.format(type))
        plt.title('Training and validation {}'.format(type))
        plt.xlabel('Epochs')
        plt.ylabel(type.capitalize())
        plt.legend()
        plt.show()

def vectorize_sequences(sequences,dimension=10000):
    results = np.zeros((len(sequences),dimension))
    for i ,sequence in enumerate(sequences):
        results[i,sequence] = 1
    return results

if __name__ == '__main__':
    # 数据来源于keras的数据集中
    (train_data, train_labels), (test_data, test_labels) = db.load_data(num_words=10)
    print("len(train_data)={}".format(len(train_data)))
    print("len(test_data)={}".format(len(test_data)))
    print("train_data[0]={}".format(train_data[0]))
    print("train_labels[0]={}".format(train_labels[0]))
    print("test_data[0]={}".format(test_data[0]))
    print("test_labels[0]={}".format(test_labels[0]))

    train_data = vectorize_sequences(train_data)
    test_data = vectorize_sequences(test_data)
    print("train_data[0]={}".format(train_data[0]))
    print("test_data[0]={}".format(test_data[0]))

    train_labels = np.asarray(train_labels).astype('float32')
    test_labels = np.asarray(test_labels).astype('float32')
    print("train_labels[0]={}".format(train_labels[0]))
    print("test_labels[0]={}".format(test_labels[0]))

    model = build_model()

    validate_train_data = train_data[:10000]
    partial_train_data = train_data[10000:]
    validate_train_lables = train_labels[:10000]
    partial_train_labels = train_labels[10000:]

    # 训练模型
    # history = model.fit(partial_train_data, partial_train_labels, epochs=10, batch_size=512,
    #                     validation_data=(validate_train_data, validate_train_lables))

    # 画图，包括损失和精度
    # draw(history)

    # 训练最终模型
    his=model.fit(train_data, train_labels, epochs=10, batch_size=512)

    # 使用测试数据测试模型
    # result = model.evaluate(test_data, test_labels)
    # print(result)

    # 预测
    predictions = model.predict(test_data)
    # print(predictions)
    print("predictions[0]={}".format(predictions[0]))
    for prediction, actual in zip(predictions, test_labels):
        print('{} : {}'.format(prediction, actual))
