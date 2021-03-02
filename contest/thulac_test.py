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
from SVM import match
from sklearn.model_selection import GridSearchCV

# 分词
# thulac(user_dict=None, model_path=None, T2S=False, seg_only=False, filt=False, deli='_')  # 初始化程序，进行自定义设置
# thu1 = thulac.thulac()  #默认模式
# text = thu1.cut("我爱北京天安门", text=True)  # 进行一句话分词
# thu1 = thulac.thulac(seg_only=True)  #只进行分词，不进行词性标注
# thu1.cut_f("input.txt", "output.txt")   #对input.txt文件内容进行分词，输出到output.txt





# 读取excel表并分词
def read_excel_divide(row, flag):
    book = xlrd.open_workbook("附件3.xlsx")
    sheet = book.sheet_by_name('Sheet1')
    thu1 = thulac.thulac(seg_only=True, rm_space = True)  # 只进行分词，不进行词性标注
    a = sheet.row_values(row)[2]
    a = a.split()
    a = str(a[0])
    text = thu1.cut(a, text=True)  # 进行一句话分词
    stopwords_remove(text, flag)


# 停用词去除
def stopwords_remove(text, flag):  # 参数表里面有个
    wordlist = []
    # 获取停用词表
    stop = open('baidu_stopwords.txt', 'r+', encoding='utf-8')
    stopword = stop.read().split("\n")
    # 遍历分词表
    for key in text.split(' '):
        # 去除停用词，去除单字，去除重复词
        if not (key.strip() in stopword) and (len(key.strip()) > 1) and not (key.strip() in wordlist):
            wordlist.append(key)
    # write_excel(wordlist, 3, 1)
    # 停用词去除END
    stop.close()
    return wordlist
    # if len(wordlist) <= 3:  # 优化 去除停用词后小于三个词的wordlist不记录，因为我发现小于三个词的基本都是有段落的很长的话并且都是一样的无用信息
    #     return
    # write_excel(wordlist, flag)


# 将分好的词写入txt
def write_excel(wordlist, flag):
    excel_path = 'test.txt'  # 文件路径
    # 将分好的词写入excel
    # excel_path=unicode('D:\\测试.xls','utf-8')  # 识别中文路径
    # rbook = xlrd.open_workbook(excel_path, formatting_info=True)  # 打开文件
    # wbook = copy(rbook)  # 复制文件并保留格式
    # w_sheet = wbook.get_sheet(0)  # 索引sheet表
    # wbook.save(excel_path)  # 保存文件
    # 将分好的词写入txt
    if flag == 1:
        rbook = open('cxjs_1.txt', 'a', encoding='UTF-8')
        for key in wordlist:
            rbook.write(key)
            rbook.write(' ')
        rbook.write('\n')
    else:
        rbook = open('test.txt', 'a', encoding='UTF-8')
        for key in wordlist:
            rbook.write(key)
            rbook.write(' ')
        rbook.write('\n')
    rbook.close()

# 样本开始位置
cxjs_begin = 1
hjbh_begin = 2011
jtys_begin = 2949
jywt_begin = 3562
ldhshbz_begin = 5151
smly_begin = 7120
wsjs_begin = 8335
# 样本个数
cxjs_num = 2009  # 城乡建设 表现良好
hjbh_num = 938  # 环境保护 表现一般
jtys_num = 613  # 交通运输 表现良好
jywt_num = 1589  # 教育文体 表现优秀
ldhshbz_num = 1969  # 劳动和社会保障 表现良好
smly_num = 1215
wsjs_num = 877
def positive_negetive():  # 找出正负样本集
    # 样本开始位置
    # global cxjs_begin, hjbh_begin, jtys_begin, jywt_begin, ldhshbz_begin, smly_begin, wsjs_begin
    # # 样本个数
    # global cxjs_num,  hjbh_num, jtys_num, jywt_num, ldhshbz_num, smly_num, wsjs_num
    # A = cxjs_num * 0.7  # 训练集测试集样本七三开 记住这个是num而不是begin。。。。
    # # 收集正负样本的单词数量各一半
    # for i in range(cxjs_begin, cxjs_begin+int(A)):  # 正样本 原本数量的70%
    #     read_excel_divide(i, 1)
    # for i in range(wsjs_begin, wsjs_begin+int(A/6)):  # 负样本 正样本数量的1/6
    #     read_excel_divide(i, 0)
    # for i in range(hjbh_begin, hjbh_begin+int(A/6)):  # 负样本
    #     read_excel_divide(i, 0)
    # for i in range(jtys_begin, jtys_begin+int(A/6)):  # 负样本
    #     read_excel_divide(i, 0)
    # for i in range(jywt_begin, jywt_begin+int(A/6)):  # 负样本
    #     read_excel_divide(i, 0)
    # for i in range(ldhshbz_begin, ldhshbz_begin+int(A/6)):  # 负样本
    #     read_excel_divide(i, 0)
    # for i in range(smly_begin,  smly_begin+int(A/6)):  # 负样本
    #     read_excel_divide(i, 0)
    for i in range(1, 1001):  # 负样本
        read_excel_divide(i, 0)


def train():  # 训练词向量，将词向量化
    sentences = gensim.models.word2vec.Text8Corpus("test.txt")  # 大哥，不要忘了手动将所有的正负样本放在一起 ###
    word2vec = Word2Vec(sentences, size=300, window=3, min_count=5, sg=1, hs=1, iter=10, workers=25)
    # word2vec = Word2Vec(sentences, sg=1, size=300, window=3, min_count=5, negative=3, sample=0.001, hs=1, workers=4)
    word2vec.save('附件3.model')


def adjusting():  # 调整参数
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    train_vec, y = match('jtys_1.txt', 'jtys_2.txt')  # 语义叠加和标签项
    model = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring='f1')
    model.fit(train_vec, y)  # 匹配
    print(model.best_params_)
    print("#######################")
    means = model.cv_results_['mean_test_score']
    params = model.cv_results_['params']
    for mean, param in zip(means, params):
        print("%f  with:   %r" % (mean, param))

# text = read_excel_divide('附件2.xlsx')  # 分词
# wordlist = stopwords_remove(text)  # 停用词去除
# 1、改A 2、改正负样本 3、改存储文件
# positive_negetive()  # 开始
# train()
# read_excel_divide(95)
# write_excel(x)  # 将分好的此存入txt
# thu1 = thulac.thulac(seg_only=True)  # 只进行分词，不进行词性标注
# pos['words'] = pos.apply(lambda x: thu1.cut(x, text=True))  # 将正样本的分词
# neg['words'] = neg.apply(lambda x: thu1.cut(x, text=True))  # 将负样本的分词
# x = np.concatenate((pos['words'], neg['words']))
# y = np.concatenate((np.ones(len(pos)), np.zeros(len(neg))))
# word2vec = Word2Vec(x, size=300, window=3, min_count=5, sg=1, hs=1, iter=10, workers=25)
# word2vec.save('../Desktop/word2vec.model')
# total_vector(x)
