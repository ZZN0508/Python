# -*- coding: utf-8 -*-
# @Time : 2020/12/23 9:41
# @Author : Zhining Zhang
# @site :
# @File : cvpr——down.py
# @main :
# @Software: PyCharm
import requests        #导入requests包
import transfrom as tf
import urllib
from bs4 import BeautifulSoup
import queue;
import os;
def get_translate_date(number):
    url = 'https://openaccess.thecvf.com/CVPR'+str(number)+'_search'
    From_data={'query':'semantic segmentation'}
    #请求表单数据
    response = requests.post(url,data=From_data)
    soup = BeautifulSoup(response.text, 'html.parser')  # 文档对象
    list_url=queue.Queue();
    list_name = queue.Queue();
    for i in soup.find_all('dt'):
        list_name.put(i.find('a').string);
    for k in soup.find_all('a'):
       if 'href' in k.attrs and '.pdf' in k['href'] and k.string=='pdf':
           list_url.put(k['href']);
    return list_url,list_name;
def download(list_url,list_name,number):
    while(list_url.empty()!=True and list_name.empty()!=True):
        suburl = list_url.get();
        name = list_name.get()
        head = "https://openaccess.thecvf.com/"
        file = "D:/贵州大学/CVPR/语义分割/"+str(number)+"/";
        u = urllib.request.urlopen(head+suburl)
        value = tf.translated_content(name, 'zh')
        print(value)
        f = open(file+value+".pdf", 'wb')
        block_sz = 999999999
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
def thread_run(list_url, list_name,number):
    import threading;
    thread_list = []
    for i in range((int)(8 * (2 + 1) / 2)):
        thread = threading.Thread(target=download, args=(list_url, list_name,number,))
        # thread = threading.Thread(target=test_thread, args=(texts_que,))
        thread.start()  # 启动线程
        thread_list.append(thread)  # 线程列表中加入线程

    for thread in thread_list:
        thread.join()  # 每个线程加入阻塞
if __name__=='__main__':
    for i in range(2014,2021):
        if not os.path.exists("D:/贵州大学/CVPR/语义分割/"+str(i)):
            os.mkdir("D:/贵州大学/CVPR/语义分割/"+str(i))
        list_url, list_name = get_translate_date(i)
        thread_run(list_url, list_name,i)
    # for i in range(len(list_url)):
    #     download(list_url[i],list_name[i]);