# -*- coding: utf-8 -*-
# @Time : 2021/1/10 15:06
# @Author : Zhining Zhang
# @site :
# @File : tree_plot.py
# @main : 绘制决策树图
# @Software: PyCharm
import matplotlib.pyplot as plt;
import tree;

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#定义文本框和箭头格式
'''决策节点的属性。boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细
可以写为decisionNode={boxstyle:'sawtooth',fc:'0.8'}'''
decisionNode = dict(boxstyle="sawtooth",fc="0.8");
#决策树叶子节点的属性
leafNode = dict(boxstyle="round4",fc="0.8");
#箭头的属性
arrow_args = dict(arrowstyle="<-");

# 绘制带箭头的注解
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    """
    为绘制图像设置文本注释添加
    :param nodeTxt: 为要显示的文本
    :param centerPt: 为文本的中心点
    :param parentPt: 为箭头指向文本的点
    :param nodeType: 决策节点的属性
    """
    # xy是箭头尖的坐标 xycoords和textcoords是坐标xy与xytext的说明（按轴坐标）若textcoords=None，则默认textcoords与xycoords相同，若都未设置，默认为data
    # va/ha设置节点框中文字的位置，va为纵向取值为(u'top', u'bottom', u'center', u'baseline')，ha为横向取值为(u'center', u'right', u'left')
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',
                            va='center',ha='center',bbox=nodeType,arrowprops=arrow_args);
def createPlot():
    """
        绘制图像函数
    """
    fig = plt.figure(1,facecolor='white');#创建一个画布，背景为白色
    fig.clf(); #画布清空
    # ax1是函数createPlot的一个属性，这个可以在函数里面定义也可以在函数定义后加入也可以
    createPlot.ax1 = plt.subplot(111,frameon=True);#frameon表示是否绘制坐标轴矩形
    plotNode('决策节点',(0.5,0.1),(0.1,0.5),decisionNode);
    plotNode('叶节点',(0.8,0.1),(0.3,0.8),leafNode);
    plt.show();

def getNumLeafs(myTree):
    """
    通过递归计算叶子节点的个数也是树的宽度
    :param myTree: 树结构
    :return: 叶子节点个数
    """
    numLeafs = 0;
    firstStr = list(myTree.keys())[0];
    secondDict = myTree[firstStr];
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key]);
        else:
            numLeafs+=1;
    return  numLeafs;

def getTreeDepth(myTree):
    """
    计算树的深度
    :param myTree:
    :return:
    """
    maxDepth = 0;
    firstStr = list(myTree.keys())[0];
    secondDict = myTree[firstStr];
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 +  getTreeDepth(secondDict[key]);
        else:
            thisDepth=1;
        if thisDepth>maxDepth:
            maxDepth =thisDepth
    return  maxDepth;

def retrieveTree(i):
    """
    返回树结构
    :param i:需要第几颗树
    :return: 返回第i颗树
    """
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head':{0:'no',1:'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i];

def plotMidText(cntrPt,parentPt,txtString):
    """
    在父子节点间填充文本信息
    :param cntrPt:当前节点的坐标
    :param parentPt:箭头指向的文本点
    :param txtString:显示内容
    """
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0];
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1];
    createPlot.ax1.text(xMid,yMid,txtString);

def plotTree(myTree,parentPt,nodeTxt):
    """
    绘制图形的坐标
    :param myTree:树结构
    :param parentPt:箭头指向的文本点
    :param nodeTxt:节点内容
    """
    # 计算宽与高
    numLeafs = getNumLeafs(myTree);
    depth = getTreeDepth(myTree);
    firstStr = list(myTree.keys())[0];
    #找到第一个中心点的位置，然后与parentPt定点进行划线
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff);
    #打印输入对应的文字
    plotMidText(cntrPt,parentPt,nodeTxt);
    plotNode(firstStr,cntrPt,parentPt,decisionNode);# 添加到画布
    secondDict = myTree[firstStr];
    #减少y的偏移，按比例减少 ，y值 = 最高点 - 层数的高度[第二个节点位置]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD;
    for key in secondDict.keys():
        # 这些节点既可以是叶子结点也可以是判断节点
        # 判断该节点是否是Node节点
        if type(secondDict[key]).__name__=='dict':
            # 如果是就递归调用
            plotTree(secondDict[key],cntrPt,str(key));
        else:
            # 如果不是，就在原来节点一半的地方找到节点的坐标
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW;# 计算节点的横坐标
            # 可视化该节点的位置
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode);#  添加到画布
            # 并打印输入对应的文字
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key));

    plotTree.yOff = plotTree.yOff+1.0/plotTree.totalD;

def createPlot(inTree):
    """
        绘制图像函数
    """
    fig = plt.figure(1,facecolor='white');#创建一个画布，背景为白色
    fig.clf(); #画布清空
    axprops = dict(xticks=[],yticks=[]);
    # ax1是函数createPlot的一个属性，这个可以在函数里面定义也可以在函数定义后加入也可以
    createPlot.ax1 = plt.subplot(111,frameon=True,**axprops);#frameon表示是否绘制坐标轴矩形
    plotTree.totalW = float(getNumLeafs((inTree)));# 获取树的宽度
    plotTree.totalD = float(getTreeDepth(inTree));# 获取树的深度
    plotTree.xOff = -0.5/plotTree.totalW;# 获取已经绘制的节点位置
    plotTree.yOff = 1.0;# 放置下一个节点的恰当位置
    plotTree(inTree,(0.5,1.0),'');
    plt.show();

if __name__=="__main__":
    #createPlot();
    myTree = retrieveTree(1);#出去树结构
    print(myTree)
    print(getNumLeafs(myTree));# 获取树结构的叶子节点数
    print(getTreeDepth(myTree));#获取树结构的深度
    createPlot(myTree);