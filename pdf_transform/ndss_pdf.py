# -*- coding: utf-8 -*-
# @Time : 2021/1/14 12:47
# @Author : Zhining Zhang
# @site :  
# @File : ndss_pdf.py
# @main : 
# @Software: PyCharm
import os
import re
import urllib

import requests

def get_context(url):
    web_context=requests.get(url)
    return web_context.text

url = 'https://www.ndss-symposium.org/ndss-program/ndss-symposium-2019-program/'
web_context=get_context(url)

name_list=re.findall(r"(?<=/\">).+(?=</a>)",web_context)    #论文名，用来保存
link_list=re.findall(r"(?<=href=\").+(?=\">Paper</a>)",web_context)    #链接地址，用来下载

print(str(link_list))
print(str(name_list))
local_dir='D:\\nudt\\NDSS2019\\'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

cnt=0

while cnt < len(link_list):
    file_name = name_list[cnt+1]  #这里加1是因为提取出来的name_list多了一个与论文名无关的name，加1才能使名字和论文链接对应起来。
    print(file_name)
    download_url = link_list[cnt]
    print(download_url)
    #将标点符号和空格替换为'_'，防止由于如:字符等不能保存文件
    file_name = re.sub('[:\?/]+',"_",file_name).replace(' ','_')
    print(file_name)
    file_path = local_dir + file_name + '.pdf'
    print(file_path)
    print(download_url)
    #download
    print('['+str(cnt)+'/'+str(len(link_list))+'] Downloading' + file_path)
    try:
        # urllib.urlretrieve(download_url, file_path)
        r = requests.get(download_url)
        with open(file_path, 'wb+') as f:
            f.write(r.content)
    except Exception:
        print('download Fail: '+file_path)
    cnt += 1
print('Finished')