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


def prepare(file_1, file_2, C, gamma, kernel):
    # word2vec = gensim.models.Word2Vec.load(file)
    train_vec, y = match(file_1, file_2)
    model = SVC(C=C, gamma=gamma, kernel=kernel)  # svm模型
    model.fit(train_vec, y)
    return model


def svm_predict(row, l, query):  # svm预测,代表列号
    global A, B, C, D, E, F, G  # 代表了其中类别的数量
    words = jieba.lcut(str(query))
    words_vec = total_vector(words)
    result = model.predict(words_vec)
    if int(result) == 1:
        if l == 0:
            writeExcel(A, l, row, 'Excel_test.xls')
            A = A + 1
        if l == 1:
            writeExcel(B, l, row, 'Excel_test.xls')
            B = B + 1
        if l == 2:
            writeExcel(C, l, row, 'Excel_test.xls')
            C = C + 1
        if l == 3:
            writeExcel(D, l, row, 'Excel_test.xls')
            D = D + 1
        if l == 4:
            writeExcel(E, l, row, 'Excel_test.xls')
            E = E + 1
        if l == 5:
            writeExcel(F, l, row, 'Excel_test.xls')
            F = F + 1
        if l == 6:
            writeExcel(G, l, row, 'Excel_test.xls')
            G = G + 1


def total_vector(words):  # 语义叠加
    vec = np.zeros(300).reshape((1, 300))
    for word in words:
        try:
            vec += word2vec.wv[word].reshape((1, 300))
        except KeyError:
            continue
    return vec


def writeExcel(row, col, str, file):
    rb = xlrd.open_workbook(file, formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row, col, str)
    wb.save(file)


A, B, C, D, E, F, G = 1, 1, 1, 1, 1, 1, 1  # 代表了其中类别的数量
# cxjs_l = []
# hjbh_l = []
# jtys_l = []
# jywt_l = []
# ldhshbz_l = []
# smly_l = []
# wsjs_l = []

# 因为每个模型不可能百分百的将一句话分出所以打算以计数的方式找热评
book = xlrd.open_workbook("附件3.xlsx")
sheet = book.sheet_by_name('Sheet1')
for row in range(1, 1000):
    a = sheet.row_values(row)[2]
    a = a.split()
    a = str(a[0])
    # 城乡建设
    word2vec = gensim.models.Word2Vec.load('cxjs.model')
    model = prepare('cxjs_1.txt', 'cxjs_2.txt', 1, 'auto', 'rbf')
    svm_predict(row, 0, a)

    # 环境保护
    word2vec = gensim.models.Word2Vec.load('hjbh.model')
    model = prepare('hjbh_1.txt', 'hjbh_2.txt', 100, 0.001, 'rbf')
    svm_predict(row, 1, a)

    # 交通运输
    word2vec = gensim.models.Word2Vec.load('jtys.model')  # jtys{C=100.0, kernel='linear'}
    model = prepare('jtys_1.txt', 'jtys_2.txt', 100, 'auto', 'linear')
    svm_predict(row, 2, a)

    # 教育文体
    word2vec = gensim.models.Word2Vec.load('jywt.model')  # jywt(C=1, kernel='linear')
    model = prepare('jywt_1.txt', 'jywt_2.txt', 1, 'auto', 'linear')
    svm_predict(row, 3, a)

    # 劳动和社会保障
    word2vec = gensim.models.Word2Vec.load('ldhshbz.model')  # ldhshbz{'C': 1, 'gamma': 0.0001, 'kernel': 'rbf'}
    model = prepare('ldhshbz_1.txt', 'ldhshbz_2.txt', 1, 0.0001, 'rbf')
    svm_predict(row, 4, a)

    # 商贸旅游
    word2vec = gensim.models.Word2Vec.load('smly.model')  # smly{'C': 1000, 'gamma': 0.0001, 'kernel': 'rbf'}
    model = prepare('smly_1.txt', 'smly_2.txt', 1000, 0.0001, 'rbf')
    svm_predict(row, 5, a)

    # 卫生计生
    word2vec = gensim.models.Word2Vec.load('wsjs.model')  # wsjs{'C': 10, 'gamma': 0.001, 'kernel': 'rbf'}
    model = prepare('wsjs_1.txt', 'wsjs_2.txt', 10, 0.001, 'rbf')
    svm_predict(row, 6, a)


# print(cxjs_l, hjbh_l)
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