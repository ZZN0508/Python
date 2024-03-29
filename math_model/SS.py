# -*- coding: utf-8 -*-
# @Time : 2020/11/24 20:45
# @Author : Zhining Zhang
# @site :  
# @File : SS.py
# @main : 
# @Software: PyCharm
# a=[[(0, 0.128), (1, 0.467), (2, 0.290), (3, 0.467), (4, 0.244), (5, 0.428), (6, 0.467)],
# [(0, 0.177), (1, 0.316), (2, 0.435), (3, 0.168), (4, 0.399), (5, 0.435), (6, 0.201), (7, 0.238), (8, 0.435), (9, 0.112)],
# [(0, 0.111), (1, 0.506), (2, 0.193), (3, 0.361), (4, 0.409), (5, 0.347), (6, 0.506), (7, 0.131)],
# [(0, 0.134), (1, 0.266), (2, 0.403), (3, 0.403), (4, 0.403), (5, 0.350), (6, 0.369), (7, 0.403)],
# [(0, 0.146), (1, 0.295), (2, 0.348), (3, 0.373), (4, 0.214), (5, 0.429), (6, 0.224), (7, 0.299), (8, 0.174), (9, 0.217), (10, 0.221), (11, 0.364)],
# [(0, 0.121), (1, 0.305), (2, 0.314), (3, 0.440), (4, 0.109), (5, 0.355), (6, 0.404), (7, 0.355), (8, 0.367), (9, 0.186)],
# [(0, 0.218), (1, 0.501), (2, 0.567), (3, 0.491), (4, 0.369)],
# [(0, 0.316), (1, 0.719), (2, 0.498), (3, 0.313), (4, 0.186)],
# [(0, 0.115), (1, 0.416), (2, 0.301), (3, 0.243), (4, 0.256), (5, 0.183), (6, 0.347), (7, 0.1377), (8, 0.17), (9, 0.416), (10, 0.336), (11, 0.327)],
# [(0, 0.094), (1, 0.337), (2, 0.346), (3, 0.429), (4, 0.166), (5, 0.322), (6, 0.275), (7, 0.2424), (8, 0.42), (9, 0.346)],
# [(0, 0.113), (1, 0.409), (2, 0.232), (3, 0.223), (4, 0.101), (5, 0.134), (6, 0.341), (7, 0.4093), (8, 0.28), (9, 0.257), (10, 0.409), (11, 0.301)]];
#
# b={'A3': 0, '一米阳光': 1, '合法': 2, '婚纱': 3, '是否': 4, '纳税': 5, '艺术摄影': 6
# ,'A6': 7, '公示': 8, '命名': 9, '咨询': 10, '城乡': 11, '成果': 12, '规划': 13, '道路': 14, '门牌': 15, '问题': 16
# ,'A7': 17, '到户': 18, '反映': 19, '春华': 20, '水泥路': 21, '自来水': 22, '镇金鼎村': 23, 'A2': 24
# ,'住户': 25, '卫生间': 26, '古道': 27, '外排': 28, '步行街': 29, '粪便': 30, '黄兴路': 31, '三期': 32
# ,'中海': 33, '中间': 34, '噪音': 35, '四期': 36, '国际': 37, '夜间': 38, '扰民': 39, '施工': 40, '社区': 41, '空地': 42, '使用': 43, '区麓': 44
# ,'单方面': 45, '小区': 46, '性质': 47, '改变': 48, '明珠': 49, '架空层': 50, '区富': 51, '房产': 52, '新村': 53, '地铁': 54
# ,'用工': 55, '质疑': 56, '违规': 57, '公交车': 58, '变道': 59
# ,'通行': 60, '随意': 61, '与麓': 62, '交汇处': 63, '保利': 64
# ,'凌晨': 65, '坡路': 66, '松路': 67, '桐梓': 68, '谷林语': 69, '东四': 70, '信号灯': 71, '太堵': 72, '建议': 73, '特立': 74, '调整': 75, '路口': 76
# ,'配时': 77, '高峰': 78, '乐果': 79, '公共': 80, '家园': 81, '摆放': 82, '炒货': 83, '空调': 84, '通道': 85, '零食': 86
# ,'青青': 87, '变压器': 88, '商学院': 89, '安装': 90, '宿舍': 91, '拆除': 92, '聚美龙楚': 93, '西地省': 94, '请求': 95, '公馆': 96, '噪声': 97, '壹号': 98}
# list_key=[]
# list_value=[]
# print(a)
# for key in b.keys():
#     list_key.append(key);
# j=0;
# for value in a:
#     list_temp=[]
#     for i in value:
#         list_temp.append((list_key[j],i[1]))
#         j+=1;
#     list_value.append(list_temp);
# # list_jiegou=[];
# # for i in range(len(list_key)):
# #     list_jiegou.append((list_key[i],list_value[i]))
# print(list_value)
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
# from matplotlib import pyplot as plt
from pylab import *

# 添加中文字体支持
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)

# 载入图像
im = cv2.imread('u=2126989626,524178143&fm=26&gp=0.jpg')

# 颜色空间转换
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# 显示原始图像
fig = plt.figure()
subplot(121)
plt.gray()
imshow(im)
title(u'彩色图', fontproperties=font)
axis('off')
# 显示灰度化图像
plt.subplot(122)
plt.gray()
imshow(gray)
title(u'灰度图', fontproperties=font)
axis('off')

show()