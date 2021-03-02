import thulac
import xlrd
import xlwt
import jieba
from xlutils.copy import copy
import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec
import gensim
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from thulac_test import stopwords_remove


# 用词语少的那句话的第一个词开始和另一句话的所有词匹配相似度，将最大的相似度加起来然后匹配
def total_vector(query):  # 语义叠加
    words = jieba.lcut(str(query))
    vec = np.zeros(300).reshape((1, 300))
    for word in words:
        try:
            vec += word2vec.wv[word].reshape((1, 300))
        except KeyError:
            continue
    return vec


# 用词语少的那句话的第一个词开始和另一句话的所有词匹配相似度，将最大的相似度加起来然后匹配
# 返回相似度
def compare(str1, str2):
    thu1 = thulac.thulac(seg_only=True, rm_space=True)
    s1 = str1.split()
    s2 = str2.split()
    s1 = str(s1[0])
    s2 = str(s2[0])
    ss1 = thu1.cut(s1, text=True)
    ss2 = thu1.cut(s2, text=True)
    ss1 = stopwords_remove(ss1)
    ss2 = stopwords_remove(ss2)
    max = 0
    sum = 0
    k = 0
    for w1 in ss1:
        try:
            for w2 in ss2:
                try:
                    s = word2vec.similarity(w1, w2)
                    # print(w1,'+',s)
                    if s > max:
                        max = s
                except KeyError:
                    continue
            if max != 0:
                sum = sum + max
                k = k + 1
            max = 0
        except KeyError:
            continue
    return sum / k


# 加载模型
word2vec = gensim.models.Word2Vec.load("cxjs.model")
# 取文件
book = xlrd.open_workbook('Excel_test.xls', formatting_info=True)
book2 = xlrd.open_workbook('附件3.xlsx')
sheet1 = book.sheet_by_name('Sheet1')
sheet2 = book2.sheet_by_name('Sheet1')
rbook = open('聚类.txt', 'a', encoding='UTF-8')
A = []
# 首先提取出第一句话然后分词去除重用词，将第一句话的语义和第二句语义进行匹配，如果大于一个标准则将其准备到一个类别下
a = int(sheet1.row_values(3)[0])
print(a)
str1 = sheet2.row_values(a)[2]
# 计算两句话的相似度然后设置阈值，超过阈值归为一类否则暂时不归类
for i in range(1, 100):
    b = int(sheet1.row_values(i)[0])
    str2 = sheet2.row_values(b)[2]
    similiar = compare(str1, str2)
    print(similiar)
    c = similiar - 0.75  # 阈值暂时设置为0.65
    if c >= 1e-5:
        A.append(b)
        print(A)
rbook.write(str(A))
rbook.write('\n')
rbook.close()




