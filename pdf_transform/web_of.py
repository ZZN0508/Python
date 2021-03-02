# -*- coding: utf-8 -*-
# @Time : 2020/12/24 21:14
# @Author : Zhining Zhang
# @site :
# @File : web_of.py
# @main :IEEE抓取
# @Software: PyCharm
# -*- coding: utf-8 -*-
import queue
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import threading;
import os

profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
           "download.default_directory": "D:\\新建文件夹"}
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_experimental_option("prefs", profile)
browser = webdriver.Chrome(chrome_options=option)
path = "D:\\新建文件夹"
dirs = os.listdir(path)
# 输出所有文件和文件夹
value_alerty = []
for file in dirs:
    value_alerty.append(file.split(".")[0])


def get_html(url):
    global browser
    browser.get(url)
    time.sleep(10)
    return browser.page_source;
def paper_number(html):
    global value_alerty
    soup = BeautifulSoup(html, 'html.parser')  # 文档对象
    img_src = soup.findAll("a", {'aria-label': 'PDF'})  # 抓取a标签
    list_pdf = [];
    for i in img_src:
        li = str(i['href']).split("arnumber=")[1]
        if  '0'+str(li) not in value_alerty:
            list_pdf.append(li);
    return list_pdf;

def download_pdf_html(list_url):
    for i in list_url:
        download_pdf("https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber="+i)

def download_pdf(url):
    global browser
    browser.get(url)

def thread_run(list_url):
    thread_list = []
    for i in range((int)(os.cpu_count()/(1-0.9))):
        thread = threading.Thread(target=run, args=(list_url,))
        thread.start()  # 启动线程
        thread_list.append(thread)  # 线程列表中加入线程

    for thread in thread_list:
        thread.join()  # 每个线程加入阻塞
def run(list_quest):
    while (list_quest.empty() != True):
        url = list_quest.get();
        html = get_html(url);
        list_url = paper_number(html);
        download_pdf_html(list_url);
if __name__ == '__main__':
    list_first_url = queue.Queue();
    for i in range(1,20):
        list_first_url.put('https://ieeexplore.ieee.org/search/searchresult.jsp?'
                       'queryText=Android%20malware&highlight=true&returnType=SEARCH&matchPubs=true&'
                       'ranges=2018_2021_Year&returnFacets=ALL&rowsPerPage=100&pageNumber='+str(i));
    run(list_first_url)
    browser.quit()

