
# -*- coding: utf-8 -*-
#梯度下降算法
#方法一 直接调用import time
"""最小二乘法"""
import numpy as np
from decimal import *
import CurveFitting as cf
# 学习率取值
learn_rate=[0.001,0.003,0.006,0.01,0.03,0.06,0.1,0.3,0.6,1,3,6,10,30,60,100,300,600];
#梯度下降求最小值
def batch_gradient_descent(list_start_xishu:list,list_xishu:list,start_point:float):
    """
    :list_start_xishu:原函数系数为list[[],[],[],...]
    :param list_xishu:梯度函数系数为list[[],[],[],...]
    :param start_point:开始点为int
    """
    np.set_printoptions(suppress=True)
    # 学习率的大小
    learn_index=0;#存放当前学习率的索引
    learn_index_max=len(learn_rate)-1;#存放当前学习率最大索引
    end_index = 3000;
    zuobiao_list=[1,1];
    while(True):
        # 计算▽J(Θi)
        list_min=get_function_value(list_xishu,start_point)
        #计算梯度下降：Θi+1=Θ0-a▽J(Θi+1)
        temp_value=Decimal(start_point)-Decimal(Decimal(learn_rate[learn_index])*list_min);
        #此时start_point为Θi，temp_value为Θi+1
        #计算Θi与Θi+1的函数值
        #list_first_value存放f(Θi)
        #list_second_value存放f(Θi+1)
        list_first_value=get_function_value(list_start_xishu, start_point)
        list_second_value=get_function_value(list_start_xishu,temp_value)

        np.set_printoptions(suppress=True)#设置print选项的参数
        print("循环系数："+str(end_index)+"x="+str(temp_value)+",y="+str(list_second_value)+"学习率："+str(learn_rate[learn_index]));
        zuobiao_list[0]=([round(float(temp_value), 6),round(float(list_second_value),6)])
        #判断梯度是否小于初始值；
        if(list_first_value>list_second_value):
            if(learn_index_max==-1 or learn_index<learn_index_max):
                learn_index+=1;
            start_point=temp_value;
        else:
            if(learn_index==0):
                return zuobiao_list;
            else:
                learn_index-=1;
                learn_index_max = learn_index;
        if(end_index<0):
            break;
        end_index-=1;
    return zuobiao_list;
# 生成y;
def getY(X):
    Y=[]
    for i in X:
       Y.append([i,2*i*i*i+3*i*i+4]);
    return Y;
#返回多元函数导数后的系数
def get_derivative(coe_value):
    list_len=len(coe_value);
    list_ret=[];
    for i in range(len(coe_value)):
        if(i<list_len-1):
            list_ret.append([float(coe_value[i]*(list_len-i-1))]);
    return np.matrix(list_ret);
#求Decimal的pow
def dec_pow(n:Decimal,k:int):
    a=1.0
    for i in range(k):
        a=Decimal(a)*n
    return float(a);
#根据自变量值求函数值
def get_function_value(list_xishu:list,value_x):
    list_min=0;
    value_x=round(float(value_x),5)
    for j in range(len(list_xishu)):
        list_min = Decimal(list_min) + Decimal(float(list_xishu[j])) * Decimal(
            dec_pow(Decimal(value_x), len(list_xishu) - j - 1));
    return list_min
if __name__ == '__main__':
    X=[];
    for i in range(-20,20):
        X.append(i);
    Y=getY(X);
    der_vlaue=cf.cureFitting(3,Y);
    print(der_vlaue)
    der_new_vlaue=get_derivative(der_vlaue);
    print(der_new_vlaue)
    func_min=batch_gradient_descent(der_vlaue,der_new_vlaue,11.0);
    print("函数最小值"+str(func_min[0][1]))
    Y.append(func_min[0]);
    print(Y)
    cf.image_rendering(Y, der_vlaue)

