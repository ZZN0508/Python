# -*- coding: utf-8 -*-
# @Time : 2020/12/2 14:47
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
import queue
import  threading;
lock = threading.Lock()
corpus=None;
num_features=None;
dictionary=None;
tfidf=None;
tf_texts=None;
buff = [];
texts=[]
list_ret_message=queue.Queue();
list_message_all=[]
# 存放各种信息
class Message:
    def __init__(self, thems, time, context, oppose, approve, count, con_time, time_long, number, user, message, hot):
        self.thems = thems;
        self.time = time;
        self.context = context;
        self.oppose = oppose;
        self.approve = approve;
        self.count = count;
        self.con_time = con_time;
        self.time_long = time_long;
        self.number = number;
        self.user = user;
        self.message = message;
        self.hot = hot;

#文件读取
def loadDataset():
    global texts;
    global list_message_all;
    dataFile = './附件3.xlsx'
    data = pd.DataFrame(pd.read_excel(dataFile,encoding='utf8')).values
    #data=data[:100]
    list_message=[]
    texts=[];
    for i in data:
        if(type(i[3])==str):
            messages=Message(i[2],datetime.datetime.strptime(i[3], '%Y/%m/%d %H:%M:%S'),i[4].replace("\n","").replace("\t",""),i[5],i[6],0,1,"",i[0],i[1],[],0);
        else:
            messages = Message(i[2], i[3], i[4].replace("\n", "").replace("\t", ""), i[5], i[6], 0,1,"",i[0],i[1],[],0);
        list_message.append(messages);
        list_message_all.append(messages);
        texts.append((i[2]).replace("\n","").replace("\t",""));
    return list_message,texts;

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
    start_time = time.time();
    # global corpus;
    global num_features;
    global dictionary
    global tfidf
    global tf_texts
    #global texts;
    # if (corpus == None):
    #     # keyword = 'A5区劳动东路魅力之城小区一楼的夜宵摊严重污染附近的空气，急需处理！时楼道里甚至整个小区都有难闻的异味。'
    #     # 1、将【文本集】生成【分词列表】
    #     texts_temp = [lcut(text) for text in texts]
    #     # 1.1、使用停用词
    #     texts_temp = delete_stop_word(texts_temp)
    #     # 2、基于文本集建立【词典】，并获得词典特征数
    #     dictionary = Dictionary(texts_temp)
    #     num_features = len(dictionary.token2id)
    #     # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    #     corpus = [dictionary.doc2bow(text) for text in texts_temp]
    #     # 4、创建【TF-IDF模型】，传入【语料库】来训练
    #     tfidf = TfidfModel(corpus)
    #     # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    #    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
    # 3.2、同理，用【词典】把【搜索词】也转换为【稀疏向量】
    list_luct = lcut(keyword)
    keyword = delete_stop_word(list_luct);
    kw_vector = dictionary.doc2bow(keyword)
    tf_kw = tfidf[kw_vector]
    # print(tf_kw)
    # 6、相似度计算
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_kw)
    # print(len(texts))
    ret_list = []
    for e, s in enumerate(similarities, 1):
        if (s >= 0.2):
            ret_list.append(e - 1);
            print('%s\n 与 \ntext%s 相似度为\n：%.2f\n\n' % (keyword, e - 1, s))

    last_time = time.time();
    print("当前线程{}".format(threading . currentThread(). ident))
    print("使用时间{}".format(last_time - start_time))
    return ret_list

list_finish=[];

# 进行迭代匹配
def iteration_message(list_message_value,text_all):
    global texts;
    global list_ret_message;
    global list_message_all;
    global list_finish;

    while(True):
        with lock:
            if len(text_all)==0:
                return ;
        list_index= similarity(text_all[0]);
        message_rep = list_message_value[0];
        del list_message_value[0];
        del text_all[0];
        message_rep.count+=len(list_index);
        max_time=0;
        list_finish.append(message_rep.number);
        # with lock:
        #     list_finish.append(message_rep.number);
        #     del list_message_value[0];
        #     del text_all[0];
        if(len(list_index)==0):
            continue;
        for index in list_index:
            if(len(list_index)>1):
                print("共有是{}，共{}".format(len(list_index),len(text_all)))
            with lock:
                message = list_message_all[index];
                if ((message.thems) in text_all):
                    index_del = text_all.index(message.thems);
                    del list_message_value[index_del]
                    del text_all[index_del]
                if(message.number not in list_finish):
                    list_finish.append(message.number);
                else:
                    continue;
            if (message.thems != message_rep.thems):
                message_rep.oppose += message.oppose;
                message_rep.approve += message.approve;
                delta = message_rep.time - message.time
                if( math.fabs(delta.days)>max_time):
                    max_time=math.fabs(delta.days)
                    message_rep.con_time=max_time
                    if delta.days > 0:
                        message_rep.time_long = str(message.time) + "至" + str(message_rep.time)
                    else:
                        message_rep.time_long = str(message_rep.time) + "至" + str(message.time)
                message_rep.message.append(message);
            elif (len(list_index) == 1 and message.thems is not list_finish):
                message_rep.time_long = str(message_rep.time) + "至" + str(message_rep.time)

        message_rep.hot = 773.514 + 0.250 * message_rep.approve + 48.269 * message_rep.count + 4.869 * message_rep.con_time
        list_ret_message.put(message_rep);

def file_add(list_message):
    # 导入CSV安装包
    import csv
    # 1. 创建文件对象
    f = open('./文件名.csv', 'w', encoding='utf-8',newline ='')
    f1 = open('./热点问题表.csv', 'w', encoding='utf-8',newline ='')
    f2 = open('./热点问题留言明细表.csv', 'w', encoding='utf-8',newline ='')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    csv_writer1 = csv.writer(f1)
    csv_writer2 = csv.writer(f2)
    # 3. 构建列表头
    csv_writer1.writerow(["热度排名", "问题ID", "热度指数","时间范围","地点/人群","问题描述"])
    csv_writer.writerow(["主题","赞成数","反对数","留言数","持续时长"]);
    csv_writer2.writerow(["问题ID","留言编号","留言用户", "留言主题", "留言时间", "留言详情", "点赞数","反对数"])
    # 4. 写入csv文件内容
    i=1;
    while(list_message.empty()!=True):
        message = list_message.get();
        csv_writer.writerow([message.thems,message.approve,message.oppose,message.count,message.con_time])
        csv_writer1.writerow([i,i,message.hot,message.time_long,'',message.thems]);
        csv_writer2.writerow(
            [i, message.number, message.user, message.thems, message.time, message.context, message.approve,
             message.oppose]);
        for m in message.message:
            csv_writer2.writerow([i, m.number, m.user, m.thems , m.time , m.context , m.approve , m.oppose]);
        i+=1;
    # 5. 关闭文件
    f.close()
    f1.close()
    f2.close()

def sort_class(list_message):
    global list_ret_message
    list_value = [];
    print("开始排序")
    while(list_message.empty()!=True):
        list_value.append(list_message.get())
    for i in range(len(list_value)):
        for j in range(i+1,len(list_value)):
            if(list_value[i].hot<list_value[j].hot):
                t = list_value[i];
                list_value[i] = list_value[j];
                list_value[j] = t;
    queue_value=queue.Queue();
    for i in list_value:
        queue_value.put(i);
    return queue_value;

# 将一个list尽量均分，前面可以分n个时则每份为n个，直到分不下为止，不限制len(list)
def EveryStrandIsN(listTemp, n):
    list_value_ret=[]
    for i in range(0, len(listTemp), n):
        list_value_ret.append(listTemp[i:i + n]);
    return list_value_ret

def npl_value():
    global corpus;
    global num_features;
    global dictionary
    global tfidf
    global tf_texts
    global texts;
    # keyword = 'A5区劳动东路魅力之城小区一楼的夜宵摊严重污染附近的空气，急需处理！时楼道里甚至整个小区都有难闻的异味。'
    # 1、将【文本集】生成【分词列表】
    texts_temp = [lcut(text) for text in texts]
    # 1.1、使用停用词
    texts_temp = delete_stop_word(texts_temp)
    # 2、基于文本集建立【词典】，并获得词典特征数
    dictionary = Dictionary(texts_temp)
    num_features = len(dictionary.token2id)
    # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts_temp]
    # 4、创建【TF-IDF模型】，传入【语料库】来训练
    tfidf = TfidfModel(corpus)
    # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
if __name__=="__main__":
    start = time.time();
    list_message,texts_que=loadDataset();
    npl_value();
    #iteration_message(list_message,texts_que)

    size = (int)(len(texts_que)/12);
    list_thread_message=EveryStrandIsN(list_message,size)
    list_thread_text = EveryStrandIsN(texts_que, size)
    thread_list = []
    print("开始创建线程")
    print(len(list_thread_message))

    for i in range(len(list_thread_message)):
        thread = threading.Thread(target=iteration_message, args=(list_thread_message[i], list_thread_text[i],))
        #thread = threading.Thread(target=test_thread, args=(texts_que,))
        thread_list.append(thread)  # 线程列表中加入线程
    for thread in thread_list:
        thread.start()  # 启动线程
    print("线程运行中")
    for thread in thread_list:
        thread.join()  # 每个线程加入阻塞

    #iteration_message(list_message,texts_que);
    list_ret_message = sort_class(list_ret_message)
    file_add(list_ret_message)
    end = time.time()  # 结束时间
    print("Tread_main：下载完成. 用时{}秒".format(end - start))

