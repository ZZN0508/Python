# -*- coding: utf-8 -*-
# import example # 引用example.py文件
from example import run # 引用xample.py文件的run方法和dictDef方法
from StandardAPI import runAPI
from ThreadDemo import runThread
if __name__ == '__main__':
    # example.run();
    # print(example.__name__)
    # run()
    # runAPI();
    runThread();
    #内置函数 dir() 用于查找模块定义的名称。 它返回一个排序过的字符串列表
    #如果没有参数，dir() 会列出你当前定义的名称:
    # print(dir(example))
    # print(dir())