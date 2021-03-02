# -*- coding: utf-8 -*-
import os
class FileOption:
    __fileObject=None;# 存放文件对象
    __filePath=None# 存放文件路径
    def __init__(self,filePath:str):
        if os.path.exists(filePath):
            self.__filePath=filePath;
        else:
            raise IOError;
    # 文件读取
    def fileRead(self):
        self.__fileObject=open(self.__filePath,'r');
        listRet=[];
        with  self.__fileObject as f:
            listRet.append(f.read());
        return ','.join(listRet);
    # 文件写入
    def fileWrite(self,listContext:list):
        self.__fileObject=open(self.__filePath,'w');
        for lists in listContext:
            self.__fileObject.write(lists+str("\n"));
        return self.__fileObject.close()==None;
    # 文件追加
    def fileAppend(self,listContext:list):
        self.__fileObject=open(self.__filePath,'a');
        for lists in listContext:
            self.__fileObject.write(lists+str("\n"));
        return self.__fileObject.close()==None;

    # 文件类销毁
    def __del__(self):
        print('销毁');








