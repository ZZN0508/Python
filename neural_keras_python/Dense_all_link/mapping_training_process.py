# -*- coding: utf-8 -*-
# @Time : 2021/1/15 21:06
# @Author : Zhining Zhang
# @site :  
# @File : mapping_training_process.py
# @main : 绘制训练过程中模型产生的数据，来反应模型的好坏
# @Software: PyCharm
import matplotlib.pyplot as plt;
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
def mappingLoss(history_dict):
    """
    训练损失和验证损失
    :param history_dict: 训练模型过程中的数据
    """
    loss_values = history_dict['loss'];# 训练集准确率
    val_loaa_values = history_dict['val_loss'];# 测试集准确率
    epochs = range(1,len(loss_values)+1);# epochs被定义为向前和向后传播中所有批次的单次训练迭代

    plt.plot(epochs,loss_values,'bo',label='训练集损失值')
    plt.plot(epochs,val_loaa_values,'b',label='测试集损失值')
    plt.title('训练和测试损失值变化图')
    plt.xlabel('单次训练迭代值')
    plt.ylabel('损失值')
    plt.legend();
    plt.show();

def mappingAcc(history_dict):
    """
    训练精度和验证精度
    :param history_dict:
    """
    plt.clf();
    if 'accuracy' in history_dict:
        acc = history_dict['accuracy'];  # 训练集损失值
        val_acc = history_dict['val_accuracy'];  # 测试集损失值
    else:
        acc = history_dict['acc'];  # 训练集损失值
        val_acc = history_dict['val_acc'];  # 测试集损失值
    epochs = range(1, len(acc) + 1);  # epochs被定义为向前和向后传播中所有批次的单次训练迭代

    plt.plot(epochs, acc, 'bo', label='训练集准确率')
    plt.plot(epochs, val_acc, 'b', label='测试集准确率')
    plt.title('训练和测试准确率变化图')
    plt.xlabel('单次训练迭代值')
    plt.ylabel('准确率')
    plt.legend();
    plt.show();

def mappingMAE(average_mae_history):
    """
    绘制每轮验证MAE图
    :param average_mae_history:
    """
    import matplotlib.pyplot as plt;

    plt.plot(range(1, len(average_mae_history) + 1), average_mae_history);
    plt.xlabel('迭代次数值')
    plt.ylabel('验证值得平均绝对误差')
    plt.title("绘制每轮验证MAE图")
    plt.show();