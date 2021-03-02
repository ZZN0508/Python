# -*- coding: utf-8 -*-
# @Time : 2020/12/23 18:19
# @Author : Zhining Zhang
# @site :  
# @File : bilibili.py
# @main : 哔哩哔哩视频下载
# @Software: PyCharm
import queue;
import os
from multiprocessing import cpu_count
def herf_get(url):
    while(url.empty()!=True):
        urls=url.get()
        print(urls)
        strs = "you-get -o D:\\贵州大学\\统计学习方法视频 -O "+str(urls[1])+" " + urls[0];
        os.system(strs)
def thread_run(list_url):
    import threading;
    thread_list = []
    for i in range((int)(cpu_count()/(1-0.9))):
        thread = threading.Thread(target=herf_get, args=(list_url,))
        # thread = threading.Thread(target=test_thread, args=(texts_que,))
        thread.start()  # 启动线程
        thread_list.append(thread)  # 线程列表中加入线程

    for thread in thread_list:
        thread.join()  # 每个线程加入阻塞
if __name__=="__main__":
    # list_que = queue.Queue();
    # for i in range(10,58):
    #     list_que.put(["https://www.bilibili.com/video/BV1o5411p7H2?p="+str(i),i]);
    # thread_run(list_que)
    strs = "you-get -o D:\\贵州大学\\统计学习方法视频 -O 42 https://www.bilibili.com/video/BV1o5411p7H2?p=42";
    os.system(strs)