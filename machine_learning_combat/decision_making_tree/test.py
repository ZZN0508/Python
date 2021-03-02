# -*- coding: utf-8 -*-
# @Time : 2021/1/10 15:40
# @Author : Zhining Zhang
# @site :  
# @File : test.py
# @main : 
# @Software: PyCharm
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8") # 决策节点的属性。boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细
# 可以写为decisionNode={boxstyle:'sawtooth',fc:'0.8'}
leafNode = dict(boxstyle="round4", fc="0.8") #决策树叶子节点的属性
arrow_args = dict(arrowstyle="<-") #箭头的属性

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
    #nodeTxt为要显示的文本，centerPt为文本的中心点，parentPt为箭头指向文本的点，xy是箭头尖的坐标，xytest设置注释内容显示的中心位置
    #xycoords和textcoords是坐标xy与xytext的说明（按轴坐标），若textcoords=None，则默认textcoords与xycoords相同，若都未设置，默认为data
    #va/ha设置节点框中文字的位置，va为纵向取值为(u'top', u'bottom', u'center', u'baseline')，ha为横向取值为(u'center', u'right', u'left')

def createPlot():
    fig = plt.figure(1, facecolor = 'white') #创建一个画布，背景为白色
    fig.clf() #画布清空
    #ax1是函数createPlot的一个属性，这个可以在函数里面定义也可以在函数定义后加入也可以
    createPlot.ax1 = plt.subplot(111, frameon = True) #frameon表示是否绘制坐标轴矩形
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()

createPlot()