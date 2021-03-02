# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
np.set_printoptions(suppress=True)
#存放去除线性相关后的矩阵
#list_last_line=[];
#曲线拟合
def cureFitting(n,lists):
    A=[];
    b = [];
    for i in range(len(lists)):
        t=[];
        for j in range(n):
            t.append(pow(lists[i][0],n-j));
        t.append(1);
        A.append(t);
        b.append([lists[i][1]]);
    print(A)
    print(b)
    # 进行拟合
    A=np.mat(A,'float32');
    b=np.mat(b,'float32');
    # 直接求解
    At = A.transpose();  # 转置变成列向量
    AtA = At.dot(A);  # 矩阵乘
    #AtAInv = np.linalg.inv(AtA)  # 求逆
    AtAInv = np.linalg.pinv(AtA+0.1/2*np.identity(np.shape(AtA)[1]))#求伪逆，如果矩阵不可逆
    AtAInvA = AtAInv.dot(At)
    x = AtAInvA.dot(b)  # 权重值
    return x;

# 散点拟合图像绘制
def image_rendering(list_point,list_coefficient):
    matplotlib.rcParams['axes.unicode_minus'] = False
    _x=[];
    _y=[];
    y_nihe=[];
    x_max=0;
    x_min=0;
    y_max=0;
    y_min=0;
    for i in range(len(list_point)):
        if(i==0):
            x_max=list_point[i][0];
            x_min=list_point[i][0];
        else:
            x_max=x_max if x_max>list_point[i][0] else list_point[i][0];
            x_min=x_min if x_min<list_point[i][0] else list_point[i][0];
        _x.append(list_point[i][0]);
        _y.append(list_point[i][1]);
        t=0;
    new_x = np.arange(x_min, x_max, 0.01)  # 可以自动生成x轴坐标，最小间隔为0.01
    for i in range(len(new_x)):
        for j in range(len(list_coefficient)):
            if(j+1==len(list_coefficient)):
                t += float(list_coefficient[j]);
            else:
                t+=float(list_coefficient[j])*pow(new_x[i],len(list_coefficient)-j-1);
        y_max = y_max if y_max > t else t;
        y_min = y_min if y_min < t else t;
        y_nihe.append(t);
        t=0;
    matplotlib.pyplot.xlabel('X')
    matplotlib.pyplot.ylabel('Y')
    matplotlib.pyplot.xlim(xmax=x_max, xmin=x_min)
    matplotlib.pyplot.ylim(ymax=y_max, ymin=y_min)
    matplotlib.pyplot.scatter(_x,_y);
    matplotlib.pyplot.scatter([_x[len(_x)-1]], [_y[len(_y)-1]], s=30, c="red", marker="s");
    matplotlib.pyplot.plot(new_x,y_nihe, c="blue");
    matplotlib.pyplot.show();
    return new_x,y_nihe;

# 如果拟合数据过多则进行多线程判断线性无关
# def thread_liner(list_value):
#     if(len(list_value)<=100):
#         list_line=if_linear_ndependence(list_value);
#         return list_line;
#     else:
#         list_thread=list_slip(list_value,100);
#         thread_pool=[];
#         print(len(list_thread))
#         for i in range(len(list_thread)):
#             t=threading.Thread(target=if_linear_ndependence,name=list_thread[i],)
#             thread_pool.append(t);
#             t.start()
#         for thread in thread_pool:
#             # 重要的一步，为什么一定要join
#             thread.join();


# 把列表平分后每份列表的的个数n
# def list_slip(listTemp, n):
#     list_ret=[]
#     for i in range(0, len(listTemp), n):
#         list_ret.append(listTemp[i:i + n]);
#     return list_ret;

