# -*- coding: utf-8 -*-
# @Time : 2020/10/20 20:48
# @Author : Zhining Zhang
# @site :  
# @File : many_gradient_descent.py
# @main : 多元梯度下降和多元最小二乘法
# @Software: PyCharm
import numpy as np;
import matplotlib;
import random;
from decimal import *;
from mpl_toolkits.mplot3d import Axes3D;
import math
np.set_printoptions(suppress=True);

#曲线拟合(最小二乘法)
def cureFitting(n,lists,lable):
    A = [];
    b = [];
    print(lists)
    for i in range(len(lists)):
        t=[];
        if(lable==1):
            for j in range(n[0]):
                t.append(pow(lists[i][0],n[0]-j));
        else:
            for j in range(len(n)):
                t.append(pow(lists[i][j], n[j]));
        t.append(1);
        A.append(t);
        b.append([lists[i][lable]]);
    print(A)
    print(b)
    # 进行拟合
    A = np.mat(A, 'float32');
    b = np.mat(b, 'float32');
    # 直接求解
    At = A.transpose();  # 转置变成列向量
    AtA = At.dot(A);  # 矩阵乘
    # AtAInv = np.linalg.inv(AtA)  # 求逆
    AtAInv = np.linalg.pinv(AtA)  # 求伪逆，如果矩阵不可逆
    AtAInvA = AtAInv.dot(At)
    x = AtAInvA.dot(b)  # 权重值
    return x;

# 学习率取值
learn_rate=[0.001,0.003,0.006,0.01,0.03,0.06,0.1,0.3,0.6,1,3,6,10,30,60,100,300,600];
#梯度下降求最小值
def batch_gradient_descent(list_start_xishu,list_start_power,list_new_xishu,list_new_power,start_point):
    """
    :param list_start_xishu: 原函数系数
    :param list_start_power: 原函数自变量次幂
    :param list_new_xishu: 导函数系数
    :param list_new_power: 导函数自变量次幂
    :param start_point:开始点
    """
    # 学习率的大小
    learn_index = 0;  # 存放当前学习率的索引
    learn_index_max = len(learn_rate) - 1;  # 存放当前学习率最大索引
    end_index = 3000;
    list_first_value = 0;
    list_second_value = 0;
    while (True):
        #1.求J'(θi)
        temp_value=[];#存放
        for i in range(len(start_point)):
            temp_value.append(Decimal(float(list_new_xishu[i]))* Decimal(dec_pow(Decimal(start_point[i]),int(list_new_power[i]))));
        T = np.mat(temp_value, 'float32');
        S = np.mat(start_point, 'float32');
        #2.求θi+1=θi-aJ'(θi)
        next_point_temp=(S-learn_rate[learn_index]*T).T;
        next_point=[];
        for i in range(len(next_point_temp)):
            next_point.append(float(str(next_point_temp[i]).replace("[",'').replace(']','')))
        #2.求J(θi),
        for i in range(len(start_point)):
            list_first_value=Decimal(list_first_value)+Decimal(float(list_start_xishu[i])) * Decimal(dec_pow(Decimal(start_point[i]),int(list_start_power[i])));
            list_second_value = Decimal(list_second_value) + Decimal(float(list_start_xishu[i])) * Decimal(dec_pow(Decimal(next_point[i]),int(list_start_power[i])));
        print("循环系数：" + str(end_index) + "x=" + str(temp_value) + ",y=" + str(list_second_value) + "学习率：" + str(
                learn_rate[learn_index]));
        #判断梯度是否小于初始值；
        if(list_first_value>list_second_value):
            if(learn_index_max==-1 or learn_index<learn_index_max):
                learn_index+=1;
            start_point=next_point;
        else:
            if(learn_index==0):
                start_point.append(list_first_value);
                return start_point;
            else:
                learn_index-=1;
                learn_index_max = learn_index;
        if(end_index<0):
            break;
        end_index-=1;
        list_first_value=0;
        list_second_value=0;
    start_point.append(list_second_value);
    return start_point;

# 多维函数求导
def derivative(list_power,list_coefficient):
    """
    :param list_power: 变量的次幂
    :param list_coefficient: 函数系数
    :return: [求导后变量的次幂，求导后函数的系数]
    """
    list_power_new=[];
    list_coefficient_new=[];
    for i in range(len(list_power)):
        list_coefficient_new.append(list_coefficient[i]*list_power[i]);
        list_power_new.append(list_power[i]-1);
    return [list_power_new,list_coefficient_new]

#求Decimal的pow

def dec_pow(n:Decimal,k:int):
    a=1.0
    for i in range(k):
        a=Decimal(a)*n
    return float(a);

#绘图
# 求出离散点的最大最小值以及散点图的横纵坐标
def image_max_min(list_point):
    list_zuobiao=[];
    list_max=[];
    list_min=[];
    zuobiao_count=len(list_point[0]);
    for i in range(zuobiao_count):
        list_zuobiao.append([])
    # 求出离散点最大值和最小值
    for i in range(len(list_point)):
        if (i == 0):
            for j in range(len(list_point[i])-1):
                list_max.append(j);
                list_min.append(j);
        else:
            for j in range(len(list_max)):
                list_max[j] = list_max[j] if list_max[j] > list_point[i][j] else list_point[i][j];
                list_min[j] = list_min[j] if list_min[j] < list_point[i][j] else list_point[i][j];
                list_zuobiao[j].append(list_point[i][j]);
            list_zuobiao[len(list_max)].append(list_point[i][len(list_max)]);
    print(list_zuobiao)
    print(list_max)
    print(list_min)
    return [list_zuobiao,list_max,list_min];

# 根据散点图求拟合函数的散点图
def image_point(list_max,list_min,list_coefficient,list_power):
    y_nihe = [];
    fun_new_point=[]
    # 根据公式生成拟合图像的坐标点
    # len_new=np.arange(list_min[0], list_max[0], 0.01)
    # fun_new_point.append(list(len_new))
    len_point_new=0;
    for i in range(len(list_max)):
        temp=list(np.arange(list_min[i],list_max[i], 0.01))
        fun_new_point.append(temp)
        if len_point_new==0:
            len_point_new = len(temp);
        elif len(temp)<len_point_new:
            len_point_new=len(temp);

    for i in range(len_point_new):
        t=0;
        if(len(list_power)<=1):
            for j in range(len(list_coefficient)):
                if (j + 1 == len(list_coefficient)):
                    t += float(list_coefficient[j]);
                else:
                    t += float(list_coefficient[j]) * pow(fun_new_point[j][i], len(list_coefficient) - j - 1);
            y_nihe.append(t);
        else:
            for j in range(len(list_coefficient)):
                if (j + 1 == len(list_coefficient)):
                    t += float(list_coefficient[j]);
                else:
                    t+=float(list_coefficient[j]) * (pow(fun_new_point[j][i], list_power[j]));
            y_nihe.append(t);
    #new_x = np.arange(x_min, x_max, 0.01)  # 可以自动生成x轴坐标，最小间隔为0.01
    fun_new_point.append(list(y_nihe))
    return fun_new_point

# 散点拟合图像绘制
def image_rendering(list_point,list_coefficient,list_power):
    matplotlib.rcParams['axes.unicode_minus'] = False
    max_min=image_max_min(list_point)
    point_fun=image_point(max_min[1], max_min[2], list_coefficient,list_power)
    fig = matplotlib.pyplot.figure()
    ax = Axes3D(fig)
    X, Y = np.meshgrid(point_fun[0],point_fun[1]);
    Z=np.array([point_fun[2]])
    print(Z)
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap='rainbow')
    list_min_point=list_point[len(list_point)-1];
    print([list_min_point[0]],[list_min_point[1]], [float(list_min_point[2])])
    ax.scatter([list_min_point[0]],[list_min_point[1]], [float(list_min_point[2])], c='r')  # 绘点
    matplotlib.pyplot.draw()
    matplotlib.pyplot.pause(10)
    matplotlib.pyplot.close()
    print(point_fun[1])

def get_y(x1=0,x2=0):
    return 3*x1*x1+4*x2*x2;

if __name__=="__main__":
    n = 5
    list_test=[];
    for i in range(4):
        x1=random.randint(-3, 3)
        x2=random.randint(-3, 3)
        list_test.append([x1,x2,get_y(x1,x2)])
        #list_test.append([x1, get_y(x1)])
    print(list_test)
    list_xishu=cureFitting([2,2],list_test,2);
    #list_xishu = cureFitting([2], list_test,1);
    print(list_xishu)
    der_list=derivative([2, 2], list_xishu)
    print(der_list[1])
    min_point=batch_gradient_descent(list_xishu,[2,2],der_list[1],der_list[0],[1,2]);
    print(min_point)
    list_test.append(min_point)
    image_rendering(list_test,list_xishu,[2,2]);
    #cureFitting(1,)

