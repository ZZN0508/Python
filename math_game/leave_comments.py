# -*- coding: utf-8 -*-
# @Time : 2020/11/28 16:11
# @Author : Zhining Zhang
# @site :  
# @File : leave_comments.py
# @main : 
# @Software: PyCharm
from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import pandas as pd;
import math;
import datetime;
import time;
import re;

# 存放各种信息
class Message:
    def __init__(self,thems,time,context,answer,answer_time,seem,ari,count,count_time):
        self.thems = thems;
        self.time = time;
        self.context = context;
        self.answer = answer;
        self.answer_time = answer_time;
        self.seem = seem;
        self.ari = ari;
        self.count = count;
        self.count_time = count_time;


#文件读取
def loadDataset():
    global texts;
    dataFile = './附件4.xlsx'
    data = pd.DataFrame(pd.read_excel(dataFile,encoding='utf8')).values
    data=data[:10]
    list_message=[];
    texts=[];
    # thems,time,context,answer,answer_time,seem,ari,count,count_time
    for i in data:
        i[5] = i[5].replace("\n", "").replace("\t", "")
        if(type(i[3])==str):
            if(type(i[6])==str):
                i[6] = datetime.datetime.strptime(i[6], '%Y/%m/%d %H:%M:%S')
            messages=Message(i[2],datetime.datetime.strptime(i[3], '%Y/%m/%d %H:%M:%S'),i[4].replace("\n","").replace("\t",""),i[5],i[6],0,0,0,0);
        else:
            if (type(i[6]) == str):
                i[6] = datetime.datetime.strptime(i[6], '%Y/%m/%d %H:%M:%S')
            messages = Message(i[2], i[3], i[4].replace("\n", "").replace("\t", ""), i[5], i[6],0,0,0,0);
        list_message.append(messages);
    return list_message;
# 进行训练
def tf_idf(texts):
    # 1、将【文本集】生成【分词列表】
    texts = [lcut(text) for text in texts]
    # 2、基于文本集建立【词典】，并获得词典特征数
    dictionary = Dictionary(texts)
    num_features = len(dictionary.token2id)
    # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]

    # 4、创建【TF-IDF模型】，传入【语料库】来训练
    tfidf = TfidfModel(corpus)
    # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】

    return dictionary,num_features,tf_texts,tfidf
# 判断是否是同一个话题
def similarity(keyword,dictionary,num_features,tf_texts,tfidf):
    start_time=time.time();
    # 用【词典】把【搜索词】也转换为【稀疏向量】
    kw_vector = dictionary.doc2bow(lcut(keyword))
    tf_kw = tfidf[kw_vector]
    # 相似度计算
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_kw)
    max_ret=0;
    for e, s in enumerate(similarities, 1):
        if s>max_ret:
            max_ret=s;
        print('kw 与 text%d 相似度为：%.2f' % (e-1, s))
    last_time = time.time();
    print("使用时间{}".format(last_time-start_time))
    return max_ret

# 可解释性计算
def ari(texts):
    zifuzongshu = len(texts);
    jushu = 1 if texts.count('。')==0 else texts.count('。');
    punctuation = '!,;:?"\'，。：；‘“、？！'
    text = re.sub(r'[{}]+'.format(punctuation), '', texts)
    zifushu = text.strip().lower()
    if(len(zifushu)==0):
        return 0;
    ARI = 4.71 *(zifuzongshu/len(zifushu))+0.5*(len(zifushu)/jushu)-21.43
    return ARI
# 信息量计算
def infor(texts):
    punctuation = '!,;:?"\'，。：；‘“、？！'
    text = re.sub(r'[{}]+'.format(punctuation), '', texts)
    zifushu = text.strip().lower()
    return 1 if len(zifushu)/100>=1 else len(zifushu)/100;
#反馈及时性
def time_quest(time1,time2):
    delta = time2-time1;
    max_time=math.fabs(delta.days)
    return max_time;

# 进行迭代匹配
def iteration_message(list_message):
    list_ret=[];
    list_texts=[]
    for i in list_message:
        list_texts.append(i.thems+i.context);
    dictionary, num_features, tf_texts, tfidf = tf_idf(list_texts)
    for i in list_message:
        #thems, time, context, answer, answer_time, seem, ari, count,count_time
        i.seem = similarity(i.answer,dictionary, num_features, tf_texts, tfidf);
        i.ari = ari(i.answer);
        i.count = infor(i.answer)
        i.count_time = time_quest(i.time,i.answer_time)
        list_ret.append(i);
    print("总长度{}".format(len(list_ret)))
    return  list_ret

def file_add(list_message,file):
    # 导入CSV安装包
    import csv
    # 1. 创建文件对象
    f = open(file, 'w', encoding='utf-8',newline='')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 3. 构建列表头
    #csv_writer.writerow(["热度排名", "问题ID", "热度指数","时间范围","地点/人群","问题描述"])
    # thems, time, context, answer, answer_time, seem, ari, count,count_time
    csv_writer.writerow(["问题","回复内容","相似度","ari","信息量","时间"]);
    # 4. 写入csv文件内容
    for message in list_message:
        csv_writer.writerow([message.thems,message.answer,message.seem,message.ari,message.count,message.count_time])
    # 5. 关闭文件
    f.close()

if __name__=="__main__":
    list_message=loadDataset();
    list_message = iteration_message(list_message);
    file_add(list_message,'./文件名.csv')