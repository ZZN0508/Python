# -*- coding: utf-8 -*-
# @Time : 2021/2/10 17:57
# @Author : Zhining Zhang
# @site :  
# @File : file_cat_dog.py
# @main : 
# @Software: PyCharm
import os;
import shutil
# 获取文件夹下的所有文件
def getFileName(path):
    list_name_dog=[]
    list_name_cat = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if 'cat' in file_name:
                list_name_cat.append(file_name);
            else:
                list_name_dog.append(file_name);
    return list_name_dog,list_name_cat;
# 创建文件
def createFile(path):
    isExists=os.path.exists(path);
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建
        return False
def moveFile(dir_file,list_name,list_file_name):
    # 6 2 2
    length = len(list_name);
    end1 = int(length * 6 / 10);
    end2 = end1 + int(length * 2 / 10);
    for i in list_name[:end1]:
        shutil.move(dir_file+ i,dir_file + list_file_name[0])
    for i in list_name[end1:end2]:
        shutil.move(dir_file+ i,dir_file + list_file_name[1])
    for i in list_name[end2:length]:
        shutil.move(dir_file+ i,dir_file + list_file_name[2])

if __name__=="__main__":
    dir_file = "D:\\贵州大学\\数据集\\dogs-vs-cats\\train\\";
    list_name_dog,list_name_cat = getFileName(dir_file);
    print(len(list_name_dog))
    print(len(list_name_cat))
    moveFile(dir_file,list_name_dog,["\\test\\dog\\","\\test1\\dog\\" ,"\\train\\dog\\"])
    moveFile(dir_file, list_name_cat, ["\\test\\cat\\", "\\test1\\cat\\", "\\train\\cat\\"])
# 创建猫狗的训练集

# 创建猫狗的测试集

# 创建猫狗的验证集
