# -*- coding: utf-8 -*-
# @Time : 2021/2/23 9:39
# @Author : Zhining Zhang
# @site :  
# @File : grabCut.py
# @main : 
# @Software: PyCharm
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(r"image\1046.jpg")
print(img.shape)
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1,65), np.float64) #以0填充的背景
fgdModel = np.zeros((1,65), np.float64)#以0填充的前景
#rect = (100,10,300,300)
rect = (1,1, 600, 430)
#grabCut(img, mask, rect, bgdModel, fgdModel, iterCount[, mode]) -> mask, bgdModel, fgdModel
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 6, cv2.GC_INIT_WITH_RECT)
#做完这些我们的掩码已经变成包含0~3的值

#将掩码中0或2 转为0（背景）， 其它（1或3）转为1（前景）
mask2 = np.where((mask==2)|(mask ==0), 255, 0).astype(np.uint8)
img1 = img*mask2[:,:, np.newaxis]#分割后的前景mask

mask2 = np.where((mask==2)|(mask ==0), 255, 1).astype(np.uint8)
img2 = img*mask2[:,:, np.newaxis]#分割后的前景最终结果

plt.subplot(121)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))#BGR模式 转RGB 模式
plt.title("grabcut")
plt.savefig('image_result/grabcut/testblueline.jpg')
plt.xticks([]); plt.yticks([]) #不显示坐标轴刻度
plt.subplot(122)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
plt.title("original")
plt.savefig('image_result/original/testblueline.jpg')
plt.xticks([]); plt.yticks([])#不显示坐标轴刻度
plt.show()
