# -*- coding: utf-8 -*-
# @Time : 2020/11/12 10:16
# @Author : Zhining Zhang
# @site :  
# @File : neural_network.py
# @main : 简单的神经网络，实现(X1 AND X2) OR ((NOT X1) AND (NOT X2))
# @Software: PyCharm

import numpy as np;
np.set_printoptions(suppress=True)
'''此类是实现与 或 非得运算'''
class NeuralNetwork:
    tricks = [];
    """A simple example class"""

    def and_function(self,initial_list):
        value_list=len(initial_list)
        initial_list = np.mat(initial_list);
        initial_list = np.insert(initial_list, 0, 1, axis=1);
        charac_value = [[value_list * -20 + 10]]
        [charac_value.append([20]) for i in range(value_list)];
        print(charac_value)
        charac_value=np.mat(charac_value);
        and_value=self.sigmoid(initial_list.dot(charac_value));
        return_value=self.if_operation_value(and_value)
        return return_value;

    def or_function(self, initial_list):
        value_list = len(initial_list)
        initial_list = np.mat(initial_list);
        initial_list = np.insert(initial_list, 0, 1, axis=1);
        charac_value = [[-10]]
        [charac_value.append([20]) for i in range(value_list)];
        charac_value = np.mat(charac_value);
        print(charac_value)
        and_value = self.sigmoid(initial_list.dot(charac_value));
        print(and_value)
        return_value = self.if_operation_value(and_value)
        return return_value;


    def not_function(self,initial_list):
        initial_list = np.mat(initial_list);
        initial_list = np.insert(initial_list, 0, 1, axis=1);
        charac_value = np.mat([[10],[-20]]);
        and_value = self.sigmoid(initial_list.dot(charac_value));
        return_value = self.if_operation_value(and_value)
        return return_value;

    # sigmoid函数
    def sigmoid(self,inX):
        return 1.0 / (1 + np.exp(-inX))

    # 根据sigmoid函数判断是1还是0
    def if_operation_value(self,value):
        if(value>0.5):
            return 1;
        else:
            return 0;

#实现(X1 AND X2) OR ((NOT X1) AND (NOT X2))
def function_custom():
    x1=1;x2=0;
    neural = NeuralNetwork();
    a1=neural.and_function([x1,x2]);
    a2=neural.not_function(x1);
    a3=neural.not_function(x2);
    a4=neural.and_function([a2,a3]);
    ret_value=neural.or_function([a1,a4]);
    return  ret_value;

if __name__=="__main__":
   ret_value = function_custom();
   print(ret_value)