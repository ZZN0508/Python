# -*- coding: utf-8 -*-
import os;
class Catalog:
    __catalogPath=None;
    __catalogObject=None;
    def __init__(self,catalogPath):
        if os.path.exists(catalogPath):
            self.__catalogPath=catalogPath;
        else:
            assert IOError;
    # 文件目录下文件列表获取
    def getCatalogList(self):
        listRet=[];
        for i,j,k in os.walk(self.__catalogPath):
            strValue=str(i);
            for l in range(len(j)):
                strValue+=str("\\")+str(j[l]);
                for m in range(len(k)):
                    listRet.append(strValue+str("\\")+str(k[m]));
        return listRet;
    # 获取文件目录下的文件夹
    def getCatalog(self):
        listRet=[];
        for i,j,k in os.walk(self.__catalogPath):
            strValue=str(i);
            if len(j)==0:
                listRet.append(strValue);
        return listRet;
