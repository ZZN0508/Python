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
# 样本开始位置
cxjs_begin = 1
hjbh_begin = 2011
jtys_begin = 2949
jywt_begin = 3562
ldhshbz_begin = 5151
smly_begin = 7120
wsjs_begin = 8335
# 样本个数
cxjs_num = 2009
hjbh_num = 938
jtys_num = 613
jywt_num = 1589
ldhshbz_num = 1969
smly_num = 1215
wsjs_num = 877


def total_vector(words):  # 语义叠加
    vec = np.zeros(300).reshape((1, 300))
    for word in words:
        try:
            vec += word2vec.wv[word].reshape((1, 300))
        except KeyError:
            continue
    return vec


TP, FN, FP, TN = 0, 0, 0, 0  # 正确和不正确个数


def svm_predict(query):  # svm预测
    global TP, FN
    words = jieba.lcut(str(query))
    words_vec = total_vector(words)
    result = model.predict(words_vec)
    if int(result) == 1:
        # print('类别：hjbh')
        TP = TP + 1
    elif int(result) == 0:
        # print('类别：其他')
        FN = FN + 1


def match(file_1, file_2):  # 向量化训练集
    i = 0
    train_vec_1 = np.zeros(300).reshape(1, 300)
    file = open(file_1, 'r', encoding='UTF-8')
    for f in file.readlines():  # 正样本语义叠加
        st = list(f.split())
        B = total_vector(st)
        if i == 0:
            train_vec_1 = B
        else:
            train_vec_1 = np.concatenate((train_vec_1, B))
        i = i + 1
    j = 0
    train_vec_2 = np.zeros(300).reshape(1, 300)  # 负样本语义叠加
    file = open(file_2, 'r', encoding='UTF-8')
    for f in file.readlines():  # 将正负样本的词语进行叠加达到语义叠加，并且将所有的样本装到一个矩阵中去
        st = list(f.split())
        B = total_vector(st)
        if j == 0:
            train_vec_2 = B
        else:
            train_vec_2 = np.concatenate((train_vec_2, B))
        j = j + 1
    train_vec = np.concatenate((train_vec_1, train_vec_2))
    y = np.concatenate((np.ones(len(train_vec_1)), np.zeros(len(train_vec_2))))
    return train_vec, y


def prepare(file, file_1, file_2, C, gamma, kernel):
    word2vec = gensim.models.Word2Vec.load(file)
    train_vec, y = match(file_1, file_2)
    model = SVC(C=C, gamma=gamma, kernel=kernel)  # svm模型
    model.fit(train_vec, y)


# word2vec = gensim.models.Word2Vec.load("cxjs.model")  # 加载词向量模型
# train_vec, y = match('jtys_1.txt', 'jtys_2.txt')  # 语义叠加和标签项
# # 预测
# model = SVC(C=1, kernel='linear')  # svm模型
# model.fit(train_vec, y)  # 匹配
# book = xlrd.open_workbook("附件2.xlsx")
# sheet = book.sheet_by_name('Sheet1')
# A = jtys_num * 0.7  # 训练集测试集样本七三开
# B = jtys_num * 0.3
# for row in range(jtys_begin+int(A), jtys_begin+jtys_num):
#     a = sheet.row_values(row)[4]
#     a = a.split()
#     a = str(a[0])
#     svm_predict(a)
# print(TP, FN)

# 计算F1-score
TP = [385, 162, 138, 437, 461, 244, 188]
TP = np.array(TP)
FN = [218, 120, 45, 40, 130, 121, 75]
FN = np.array(FN)
FP = [35, 3, 31, 20, 26, 44, 10]
FP = np.array(FP)
TN = [567, 278, 152, 456, 564, 320, 253]
TN = np.array(TN)
F = 0
for i in range(7):
    P = TP[i]/(TP[i]+FP[i])
    R = TP[i]/(TP[i]+FN[i])
    F += 2*P*R/(P+R)
    print(P, R, 2*P*R/(P+R))
F1 = F/7
print(F1)

# cxjs(C=1000, gamma=0.0001, kernel='rbf')
# TP = 385 FN = 218
# FP = 35 TN = 567
# hjbh{'C': 100, 'gamma': 0.001, 'kernel': 'rbf'}
# TP = 162 FN = 120
# FP = 3 TN = 278
# jtys{C=100.0, kernel='linear'}
# TP = 138 FN = 45
# FP = 31 TN = 152
# jywt(C=1, kernel='linear')
# TP = 437 FN = 40
# FP = 20 TN = 456
# ldhshbz{'C': 1, 'gamma': 0.0001, 'kernel': 'rbf'}
# TP = 461 FN = 130
# FP = 26 TN = 564
# smly{'C': 1000, 'gamma': 0.0001, 'kernel': 'rbf'}
# TP = 244 FN = 121
# FP = 44 TN = 320
# wsjs{'C': 10, 'gamma': 0.001, 'kernel': 'rbf'}
# TP = 188 FN = 75
# FP = 10 TN = 253
