# -*- coding: utf-8 -*-
class MyClass:
    tricks=[];
    """A simple example class"""
    def __init__(self, realpart):
        self.r = realpart;
    def f(self):
        return 'hello world';
    def add_trick(self, trick):
        self.tricks.append(trick)
class YouClass:
    def __init__(self):
        print("这是你的类")
    def f(self):
        return '这是你的类';
# 继承
class HeClass(MyClass):
    def __init__(self):
        print("这是派生类");
        super().__init__(3);
# 多重继承
class SheClass(MyClass,YouClass):
    value=45;
    def __init__(self):
        print("这是多重继承后的派生类");
    __value=value;# 变量前面加两个下划线表示该变量为私有变量
if __name__=='__main__':
    x = MyClass(1);
    print(x.f());
    print(x.r);
    x.add_trick(23);
    print(x.tricks);# [23]
    y = MyClass(2);
    y.add_trick(34);
    print(y.tricks);# [23, 34]

    z=HeClass();
    z.add_trick(56)
    print(z.tricks);# [23, 34, 56]

    m=SheClass();
    m.add_trick(90)
    print(m.tricks);# [23, 34, 56]
    # print(m.__value);
