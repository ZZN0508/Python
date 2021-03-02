# -*- coding: utf-8 -*-
# @Time : 2021/1/11 16:27
# @Author : Zhining Zhang
# @site :  
# @File : tree_practice.py
# @main : 使用决策树预测隐形眼镜类型
# @Software: PyCharm
import tree;
import tree_plot
def lenses():
    fr = open('lenses.txt');
    lenses = [inst.strip().split('\t') for inst in fr.readlines()];
    lensesLabels = ['age','prescript','astigmatic','tearRate'];
    lensesTree = tree.createTree(lenses,lensesLabels);
    print(lensesTree);
    tree_plot.createPlot(lensesTree);

if __name__=="__main__":
    lenses();
