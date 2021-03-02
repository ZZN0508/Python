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
from jieba import lcut
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity
import threading
import time
from sklearn.svm import SVC
from SVM import match
from sklearn.model_selection import GridSearchCV


# 写入excel
def writeExcel(row, col, str1, file):
    rb = xlrd.open_workbook(file, formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row, col, str1)
    wb.save(file)


# 制作字典，并且计算频率值,将频率值写到excel中
def tf_idf(texts):
    # # 1、将【文本集】生成【分词列表】
    # texts = [lcut(text) for text in texts]
    # 2、基于文本集建立【词典】，并获得词典特征数
    dictionary = Dictionary(texts)
    # num_features = len(dictionary.token2id)
    rbook = open('2.txt', 'a', encoding='UTF-8')
    # 写入词典内容
    rbook.write(str(dictionary.token2id))
    rbook.write("\n")
    # 将频率从多到少写入excel
    i = 1
    for key, value in dictionary.dfs.items():
        str1 = str(key)+ " " +str(value)
        writeExcel(i, 0, str1, "3.xls")
        i = i + 1
    rbook.close()


# 读取excel表并分词
def read_excel_divide(row):
    book = xlrd.open_workbook("附件2.xlsx")
    sheet = book.sheet_by_name('Sheet1')
    a = sheet.row_values(row)[4]
    a = a.split()
    a = str(a[0])
    text = jieba.lcut(a)  # 进行一句话分词
    stopwords_remove(text)


# 停用词去除
def stopwords_remove(text):  # 参数表里面有个
    wordlist = []
    stop = open('baidu_stopwords.txt', 'r+', encoding='utf-8')
    stopword = stop.read().split("\n")
    for key in text:
        # 去除停用词，去除单字，去除重复词
        if not (key.strip() in stopword) and (len(key.strip()) > 1) and not (key.strip() in wordlist):
            wordlist.append(key)
    stop.close()
    # write_excel(wordlist)
    return wordlist


# 将分好的词写入txt文件并且写成一行的形式
def write_excel(wordlist):
    rbook = open('2.txt', 'a', encoding='UTF-8')
    for key in wordlist:
        rbook.write(key)
        rbook.write(' ')
    # rbook.write('\n')


# 计算TF-IDF
def npl_value(texts):
    # keyword = 'A5区劳动东路魅力之城小区一楼的夜宵摊严重污染附近的空气，急需处理！时楼道里甚至整个小区都有难闻的异味。'
    # 1、将【文本集】生成【分词列表】
    texts = [lcut(text) for text in texts]
    # 2、基于文本集建立【词典】，并获得词典特征数
    dictionary = Dictionary(texts)

    # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 4、创建【TF-IDF模型】，传入【语料库】来训练
    tf_idf_model = TfidfModel(corpus, normalize=False)
    # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    word_tf_tdf = list(tf_idf_model[corpus])
    print('词的tf-idf值:', word_tf_tdf)




# # 启动分词，去除停用词
# for i in range(1, 30):
#     read_excel_divide(i)
#
#
# 计算词频
# list0 = []
# rbook = open('2.txt', 'r', encoding='UTF-8')
# for key in rbook.readlines():
#     list0.append(key.split(" "))
# rbook.close()
# tf_idf(list0)


# keyword = "A5区劳动东路魅力之城小区一楼的夜宵摊严重污染附近的空气，急需处理！时楼道里甚至整个小区都有难闻的异味。"
# 计算TF-IDF
# npl_value(keyword)
# similiar(keyword)
#
# list_luct = lcut(keyword)
# keyword = stopwords_remove(list_luct)
# dictionary = Dictionary(['human', 'interface', 'computer'])
# print(dictionary.token2id)
# # num_features = len(dictionary.token2id)
# # corpus = [dictionary.doc2bow(text) for text in keyword]
