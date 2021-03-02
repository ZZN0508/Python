# -*- coding: utf-8 -*-
# @Time : 2020/11/29 11:57
# @Author : Zhining Zhang
# @site :  
# @File : question_classify.py
# @main : 留言分类
# @Software: PyCharm
# 读取excel表并分词
import xlrd;
import thulac;
import gensim;
import word2Vec;
import numpy as np;
import GridSearchCV;
import SVC;
import match;
def read_excel_divide(row, flag):
    book = xlrd.open_workbook("附件3.xlsx")
    sheet = book.sheet_by_name('Sheet1')
    thu1 = thulac.thulac(seg_only=True, rm_space = True)
    a = sheet.row_values(row)[2]
    a = a.split()
    a = str(a[0])
    text = thu1.cut(a, text=True)
    stopwords_remove(text, flag)

# 停用词去除
def stopwords_remove(text):  # 参数表里面有个
    wordlist = []
    # 获取停用词表
    stop = open('baidu_stopwords.txt', 'r+', encoding='utf-8')
    stopword = stop.read().split("\n")
    # 遍历分词表
    for key in text.split(' '):
        # 去除停用词，去除单字，去除重复词
        if not (key.strip() in stopword) and (len(key.strip()) > 1) and not (key.strip() in wordlist):
            wordlist.append(key)
    stop.close()
    return wordlist

# 训练词向量，将词向量化
def train():
    sentences = gensim.models.word2vec.Text8Corpus("test.txt")
    word2vec = word2Vec(sentences, size=300, window=3, min_count=5, sg=1, hs=1, iter=10, workers=25)
    word2vec.save('附件3.model')

# 语义叠加
def total_vector(words):
    vec = np.zeros(300).reshape((1, 300))
    for word in words:
        try:
            vec += word2Vec.wv[word].reshape((1, 300))
        except KeyError:
            continue
    return vec

#模型
def prepare(file, file_1, file_2, C, gamma, kernel):
    word2vec = gensim.models.Word2Vec.load(file)
    train_vec, y = match(file_1, file_2)
    model = SVC(C=C, gamma=gamma, kernel=kernel)  # svm模型
    model.fit(train_vec, y)

# 参数调节
def Adjust_parameters():
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    train_vec, y = match('jtys_1.txt', 'jtys_2.txt')  # 语义叠加和标签项
    model = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring='f1')
    model.fit(train_vec, y)  # 匹配正负样本
    print(model.best_params_)
    print("#######################")
    means = model.cv_results_['mean_test_score']
    params = model.cv_results_['params']
    for mean, param in zip(means, params):
        print("%f  with:   %r" % (mean, param))

# F1计算
def F1_socre(TP,FN,FP,TN):
    F = 0
    for i in range(7):
        P = TP[i]/(TP[i]+FP[i])
        R = TP[i]/(TP[i]+FN[i])
        F += 2*P*R/(P+R)
        print(P, R, 2*P*R/(P+R))
    F1 = F/7