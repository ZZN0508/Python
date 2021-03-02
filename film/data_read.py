# -*- coding: utf-8 -*-
# @Time : 2020/10/25 15:33
# @Author : Zhining Zhang
# @site :  
# @File : data_read.py
# @main : 获取电影票房和评分以及是否是好电影
# @Software: PyCharm
from bs4 import BeautifulSoup;
import pandas as pd;
import requests;


def sgw(year):
    s = requests.session();
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'movie.mtime.com',
        'Referer': 'http://movie.mtime.com/boxoffice/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.15 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    };
    s.headers.update(headers);
    df = pd.DataFrame(columns=('排名', '电影','评分', '类型', '首日票房（元）', '年度票房（元）', '上映日期'));
    x = 0;
    for m in range(len(year)):
        for i in range(10):
            url = 'http://movie.mtime.com/boxoffice/?year={}&area=china&type=MovieRankingYear&category=all&page={}&display=table&timestamp=1547015331595&version=07bb781100018dd58eafc3b35d42686804c6df8d&dataType=json'.format(
                str(year[m]),str(i));
            req = s.get(url=url, verify=False).text;
            bs = BeautifulSoup(req, 'lxml');
            tr = bs.find_all('tr');
            for j in tr[1:]:
                td = j.find_all('td');
                list = [];
                bol=False;
                for k in range(6):
                    if k == 1:
                        nm = td[k].find('a').text;
                        print(td[k].a.string);
                        list.append(nm);
                        if td[k].find("div")==None:
                            bol=True;
                            break;
                        else:
                            list.append(td[k].find("div").text.replace("<em>","").replace("</em>",""));
                    else:
                        list.append(td[k].text);
                if bol==False:
                    df.loc[x] = list;
                    x = x + 1;
    print(df);
    df.to_excel('时光网.xlsx', index=False, encoding="GB18030");

sgw([2017,2018,2019]);