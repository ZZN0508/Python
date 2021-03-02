# -*- coding: utf-8 -*-
# @Time : 2020/11/21 10:40
# @Author : Zhining Zhang
# @site :  
# @File : test.py
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

corpus=None;
num_features=None;
dictionary=None;
tfidf=None;
tf_texts=None;
buff = [];
texts=[]

# 存放各种信息
class Message:
    def __init__(self,thems,time,context,oppose,approve,count,con_time,time_long):
        self.thems = thems;
        self.time = time;
        self.context = context;
        self.oppose = oppose;
        self.approve = approve;
        self.count = count;
        self.con_time = con_time;
        self.time_long = time_long;

#文件读取
def loadDataset():
    global texts;
    dataFile = './附件3.xlsx'
    data = pd.DataFrame(pd.read_excel(dataFile,encoding='utf8')).values
    #data=data[:10]
    list_message=[];
    texts=[];
    for i in data:
        if(type(i[3])==str):
            messages=Message(i[2],datetime.datetime.strptime(i[3], '%Y/%m/%d %H:%M:%S'),i[4].replace("\n","").replace("\t",""),i[5],i[6],0,1,"");
        else:
            messages = Message(i[2], i[3], i[4].replace("\n", "").replace("\t", ""), i[5], i[6], 0,1,"");
        list_message.append(messages);
        texts.append((i[2]+i[4]).replace("\n","").replace("\t",""));
    return list_message,texts;
buff=[];
# 去除停用词
def delete_stop_word(texts):
    global buff
    if(len(buff)==0):
        import codecs;
        with codecs.open('./test.txt', encoding='utf-8') as fp:
            for ln in fp:
                el = ln[:-2]
                buff.append(el)
    texts_temp = []
    for words in texts:
        if(type(words)==list):
            word_list = []
            for word in words:
                if word not in buff and len(word) > 1:
                    word_list.append(word);
            texts_temp.append(word_list)
        else:
            if words not in buff and len(words) > 1:
                texts_temp.append(words);

    return texts_temp;

# 判断是否是同一个话题
def similarity(keyword):
    start_time=time.time();
    global corpus;
    global num_features;
    global dictionary
    global tfidf
    global tf_texts
    global buff;
    global texts;
    if(corpus==None):
        #keyword = 'A5区劳动东路魅力之城小区一楼的夜宵摊严重污染附近的空气，急需处理！时楼道里甚至整个小区都有难闻的异味。'
        # 1、将【文本集】生成【分词列表】
        texts = [lcut(text) for text in texts]
        # 1.1、使用停用词
        texts = delete_stop_word(texts)
    # 2、基于文本集建立【词典】，并获得词典特征数
    dictionary = Dictionary(texts)
    num_features = len(dictionary.token2id)
    # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 4、创建【TF-IDF模型】，传入【语料库】来训练
    tfidf = TfidfModel(corpus)
    # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
    # 3.2、同理，用【词典】把【搜索词】也转换为【稀疏向量】
    list_luct=lcut(keyword)
    keyword = delete_stop_word(list_luct);
    kw_vector = dictionary.doc2bow(keyword)
    tf_kw = tfidf[kw_vector]
    #print(tf_kw)
    # 6、相似度计算
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_kw)
    #print(len(texts))
    ret_list=[]
    for e, s in enumerate(similarities, 1):
        if(round(s,3)>=0.28):
            ret_list.insert(0,e-1);
            #print('kw 与 text%d 相似度为：%.2f' % (e-1, s))
        if(s>=0.28):
            print("{},\n{}".format(texts[e-1],s))
    last_time = time.time();
    print("使用时间{}".format(last_time-start_time))
    return ret_list
# 进行迭代匹配
def iteration_message(list_message,text_all):
    global texts;
    list_ret_message=[];
    while(len(text_all)>1):
        list_equ_messages=[];
        list_index= similarity(text_all[0]);
        message_rep = list_message[0];
        message_rep.count+=len(list_index);
        max_time=0;
        if(len(list_index)==0):
            list_ret_message.append(list_message[0]);

            list_equ_messages.append(list_message[0])
            file_add(list_equ_messages,str(time.time())+".csv")

            del list_message[0];
            del texts[0];
            del text_all[0];

            continue;
        for index in list_index:
            message = list_message[index];
            message_rep.oppose+=message.oppose;
            message_rep.approve+= message.approve;
            delta = message_rep.time - message.time
            if( math.fabs(delta.days)>max_time):
                max_time=math.fabs(delta.days)
                message_rep.con_time=max_time
                message_rep.time_long=str(message_rep.oppose)+"至"+str(message_rep.approve)
            list_equ_messages.append(message);
            del list_message[index];
            del texts[index];
            del text_all[index];
        file_add(list_equ_messages,str(time.time())+".csv")
        list_ret_message.append(message_rep);
    list_ret_message.append(list_message[0]);
    return list_ret_message;

def file_add(list_message,file):
    # 导入CSV安装包
    import csv
    # 1. 创建文件对象
    f = open('cvs_file/'+file, 'w', encoding='utf-8',newline='')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 3. 构建列表头
    #csv_writer.writerow(["热度排名", "问题ID", "热度指数","时间范围","地点/人群","问题描述"])
    csv_writer.writerow(["赞成数","反对数","留言数","持续时长","问题描述"]);
    # 4. 写入csv文件内容
    i=1;
    for message in list_message:
        csv_writer.writerow([message.approve,message.oppose,message.count,message.con_time,message.thems])
    # 5. 关闭文件
    f.close()
if __name__=="__main__":

    list_message,texts=loadDataset();
    list_message = iteration_message(list_message,texts);
    file_add(list_message,'./文件名.csv')


