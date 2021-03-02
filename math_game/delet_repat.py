# -*- coding: utf-8 -*-
# @Time : 2021/1/26 19:45
# @Author : Zhining Zhang
# @site :  
# @File : delet_repat.py
# @main : 
# @Software: PyCharm
import codecs;
def getWrite():
    strs="";
    list_word=[]
    with codecs.open('./8873.txt', encoding='utf-8') as fp:
        for ln in fp:

            strs+=ln;
            if '-------' in ln:
                list_word.append(strs);
                strs="";
    print(len(list_word))
    return list_word;

from difflib import SequenceMatcher
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def setRead(list_word):
    with open("new.txt", "w",encoding='utf-8') as f:
        for i in list_word:
            f.write(i.strip())
            f.write("\n")
if __name__=="__main__":
    list_word=getWrite();
    length = len(list_word);
    i=0
    while(i<length):
        j = i+1;
        while(j<length):
            values = similarity(list_word[i].replace('\n', "").strip(), list_word[j].replace('\n', "").strip());
            if (values >= 0.5):
                del list_word[j];
                j = j - 1;
                length = len(list_word);
            j+=1;
        i+=1;
        print(i)
    setRead(list_word)
    import os;

    os.system('shutdown -s -f -t 59')