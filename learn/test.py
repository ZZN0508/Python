# -*- coding: utf-8 -*-
# @Time : 2020/11/6 10:10
# @Author : Zhining Zhang
# @site :  
# @File : test.py
# @main : 测试代码
# @Software: PyCharm

import numpy as np
import matplotlib.pyplot as plt

def create_datas():
    '''
    生成10个待拟合的点
    :return: xs, ys
    '''
    xs = np.arange(0.1, 4, 0.1)
    # y = ln(2x) + noize,  -1 <= noize <= 1
    ys = np.array([np.log(x * 2) + 2 + np.random.uniform(-1, 1) for x in xs])

    return xs, ys

class Regression():
    ''' 回归类 '''
    def __init__(self, xs, ys):
        '''
        :param xs: 输入数据的特征集合
        :param ys: 输入数据的标签集合
        '''
        self.xs, self.ys = xs, ys
        self.theta = None # 模型参数

    def train_datas(self, xs=None):
        '''
        重新构造训练样本的特征和标签
        :param xs: 输入数据的特征集合
        :return: 矩阵形式的训练样本特征和标签
        '''
        xs = self.xs if xs is None else xs
        X = self.train_datas_x(xs)
        Y = np.c_[ys] # 将ys转换为m行1列的矩阵
        return X, Y

    def train_datas_x(self, xs):
        '''
        重新构造训练样本的特征
        :param xs: 输入数据的特征集合
        :return: 矩阵形式的训练样本特征
        '''
        m = len(xs)
        # 在第一列添加x0,x0=1,并将二维列表转换为矩阵
        X = np.mat(np.c_[np.ones(m), xs])
        return X

    def fit(self):
        ''' 数据拟合 '''
        X, Y = self.train_datas()
        self.theta = (X.T * X).I * X.T * Y

    def predict(self, xs):
        '''
        根据模型预测结果
        :param xs: 输入数据的特征集合
        :return: 预测结果
        '''
        X = self.train_datas(xs=xs)[0]
        return self.theta.T * X.T

    def show(self):
        ''' 绘制拟合结果 '''
        plt.figure()
        plt.scatter(self.xs, self.ys, color='r', marker='.', s=10)  # 绘制数据点
        self.show_curve(plt) # 绘制函数曲线
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis('equal')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 解决中文下的坐标轴负号显示问题
        plt.legend(['拟合曲线', '样本点'])
        plt.show()

    def show_curve(self, plt):
        ''' 绘制函数曲线 '''
        pass

    def global_fun(self):
        ''' 返回目标函数 '''
        gf = ['(' + str(t[0, 0]) + str(i) + ')x^' + str(i) for i, t in enumerate(self.theta)]
        return ' + '.join(gf)

class Linear(Regression):
    ''' 线性模型'''
    def show_curve(self, plt):
        '''
        绘制拟合结果
        :param plt: 输入数据的特征集合
        '''
        xx = [self.xs[0], self.xs[-1]]
        yy = self.predict(xx)
        plt.plot(xx, np.array(yy)[0])

class Multinomial(Regression):
    ''' 多项式回归模型 '''
    def __init__(self, xs, ys, n=3):
        '''
        :param xs: 输入数据的特征集合
        :param ys: 输入数据的标签集合
        :param n: 多项式的项数
        '''
        super().__init__(xs, ys)
        self.n = n

    def train_datas_x(self, xs):
        '''
        重新构造训练样本的特征
        :param xs: 输入数据的特征集合
        :return: 矩阵形式的训练样本特征
        '''
        X = super().train_datas_x(xs)
        for i in range(2, self.n + 1):
            X = np.column_stack((X, np.c_[xs ** i])) # 构造样本的其他特征
        return X

    def show_curve(self, plt):
        ''' 绘制函数曲线 '''
        xx = np.linspace(self.xs[0], self.xs[-1], len(self.xs) * 20)
        yy = self.predict(xx)
        plt.plot(xx, np.array(yy)[0], '-')

if __name__ == '__main__':
    xs, ys = create_datas()
    regressions = [Linear(xs, ys), Multinomial(xs, ys), Multinomial(xs, ys, n=5), Multinomial(xs, ys, n=10)]
    for r in regressions:
        r.fit()
        r.show()
        print(r.global_fun())

