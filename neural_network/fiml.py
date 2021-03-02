# -*- coding: utf-8 -*-
# @Time : 2020/11/26 10:52
# @Author : Zhining Zhang
# @site :  
# @File : fiml.py
# @main : 好电影差电影分类
# @Software: PyCharm
import xlrd
import matplotlib.pyplot as plt
from numpy import *
import keras as ks;
import queue;
import time;

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# 读取数据（这里只有两个特征）, 是由X1和X2，y组成
def data_settle():
    # 打开文件方式1：
    work_book = xlrd.open_workbook('D:\\GuiZhouUniversity\\Python\\film\\时光网.xlsx')
    sheets_name = work_book.sheet_by_name('Sheet1')
    list_score=[];
    list_price=[];
    data_col = [sheets_name.col_values(i) for i in range(sheets_name.ncols)]
    del(data_col[1][0])
    del(data_col[2][0])
    del(data_col[5][0])
    list_name=data_col[1];
    for i in data_col[2]:
        list_score.append(float(i));

    for i in data_col[5]:
        if '亿' in i:
            list_price.append(float(i.replace("亿","")));
        elif '万' in i :
            temp=i.replace("万","");
            list_price.append(float(temp)/10000);
    dataMat=[];
    labelMat=[];
    for i in range(len(list_price)):
        if(list_score[i]<6):
            dataMat.append([list_price[i],list_score[i]]);
            labelMat.append(-1)
        else:
            dataMat.append([list_price[i], list_score[i]]);
            labelMat.append(1)

    return dataMat,labelMat;
# 循环拿取list中的元素
def loop_request(list_value,list_ret):
    for i in list_value:
        if type(i)==list or type(i)==ndarray:
            loop_request(i,list_ret);
        else:
            list_ret.append(i);
    return list_ret
# 模型训练
def model_drill(X,Y,quert,start_index,end_index):
    train_data =X[0:80];
    train_lable = Y[:80]
    test_data = X[80:];
    test_labels = Y[80:];

    model = ks.models.Sequential();
    out_len=(int)(math.log(len(X),2))
    for i in range(start_index,end_index):
        model.add(ks.layers.Dense(i,input_shape=(2,),activation='relu'));
        model.add(ks.layers.Dense(i, activation='relu'));
        model.add(ks.layers.Dense(i, activation='relu'));
        model.add(ks.layers.Dense(i, activation='relu'));
        model.add(ks.layers.Dense(i, activation='relu'));
        model.add(ks.layers.Dense(i, activation='relu'));
        model.add(ks.layers.Dense(1, activation='sigmoid'))

        '''随机梯度下降法，支持动量参数，支持学习衰减率，支持Nesterov动量
            lr：大或等于0的浮点数，学习率
            momentum：大或等于0的浮点数，动量参数
            decay：大或等于0的浮点数，每次更新后的学习率衰减值
            nesterov：布尔值，确定是否使用Nesterov动量
        '''
        sgd = ks.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        # 使用梯度下降算法进行优化，使用交叉熵作为损失函数，并计算其正确率
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        # model.compile(optimizer='adam',
        #           loss='binary_crossentropy',
        #           metrics=['accuracy'])
        model.fit(train_data,train_lable,epochs=100, batch_size=521);
        model.summary()

        weights = array(model.get_weights())
        list_weights = loop_request(model.layers[2].get_weights(),[])
        # 预测
        predictions = model.predict(test_data)
        # print(predictions)
        print("predictions[0]={}".format(predictions[0]))
        count =0;
        for prediction, actual in zip(predictions, test_labels):
            if(prediction<0.5 and test_labels==-1):
                count++1;
            print('{} : {}'.format(prediction, actual))
        quert.put([start_index,count])
    return  list_weights;

def thread_start(train_data,train_lable,qu):
    import threading
    thread_list=[];
    #（线程等待时间与线程CPU时间之比 + 1）*CPU数目
    # 比如平均每个线程CPU运行时间为0.5s，而线程等待时间（非CPU运行时间，比如IO）为1.5s，CPU核心数为8，那么根据上面这个公式估算得到：((0.5+1.5)/0.5)*8=32
    from multiprocessing import cpu_count
    len_thread=(int)(((6.5+1)/6.5)*cpu_count())
    start_number =1;
    for i in range(len_thread):
        thread = threading.Thread(target=model_drill, args=(train_data,train_lable,qu,start_number,(int)(100/len_thread)+start_number))
        start_number=(int)(100/len_thread);
        # thread = threading.Thread(target=test_thread, args=(texts_que,))
        thread_list.append(thread)  # 线程列表中加入线程
    for thread in thread_list:
        thread.start()  # 启动线程
    print("线程运行中")
    for thread in thread_list:
        thread.join()  # 每个线程加入阻塞
    max_count=qu.get();
    while(qu.empty()!=True):
        test = qu.get();
        if(test[1]>max_count[1]):
            max_count=test;
    print(max_count)
if __name__=="__main__":
    train_data,train_lable=data_settle();
    qu = queue.Queue();

    start=time.time();
    thread_start( train_data,train_lable,qu)
    #test_data=model_drill(train_data,train_lable,qu,1)
    print(time.time()-start)
    # list_value=[1,2,[3,4,[5]],[6,[7],[8]]];
    # print(loop_request(list_value,[]));
