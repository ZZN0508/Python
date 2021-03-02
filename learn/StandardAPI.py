# -*- coding: utf-8 -*-
def systemDef():
    import os;
    # os 模块提供了许多与操作系统交互的函数
    print(os.getcwd());# 获取当前文件的物理位置
    os.chdir('../.idea');# 更改当前工作目录
    os.system('mshta vbscript:msgbox("我是提示内容",64,"我是提示标题")(window.close)');# 在系统shell中运行指定命令
    # dir(object)
    # 如果没有实参，则返回当前本地作用域中的名称列表。如果有实参，它会尝试返回该对象的有效属性列表。
    print(dir(os));
    # help(object)
    # 启动内置的帮助系统（此函数主要在交互式中使用）。如果没有实参，解释器控制台里会启动交互式帮助系统。如果实参是一个字符串，则在模块、函数、类、方法、关键字或文档主题中搜索该字符串，并在控制台上打印帮助信息。如果实参是其他任意对象，则会生成该对象的帮助页。
    print(help(os));

def commandLine():
    import sys
    print(sys.argv)
    print( sys.stderr.write('这是个警告\n'))
def stringRe():
    import re
    print(re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest'));# ['foot', 'fell', 'fastest']
    print(re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat'));# cat in the hat
    import reprlib
    s=reprlib.repr(set('3473423423dfdf453454edggsd'))
    print(set('3473423423dfdf453454edggsd'))# {'d', '5', 'g', 'f', '2', '4', '3', '7', 'e', 's'}
    print(s)# {'2', '3', '4', '5', '7', 'd', ...}
    import pprint
    t = [[[['black', 'cyan'], 'white', ['green', 'red']], [['magenta',
                                                            'yellow'], 'blue']]]

    pprint.pprint(t, width=30)
    import textwrap
    doc = """The wrap() method is just like fill() except that it returns
    a list of strings instead of one big string with newlines to separate
    the wrapped lines."""
    print(textwrap.fill(doc, width=40))

    import locale
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')

    conv = locale.localeconv()          # get a mapping of conventions
    x = 1234567.8
    s=locale.format("%d", x, grouping=True)
    print(s)
    s=locale.format_string("%s%.*f", (conv['currency_symbol'],
                                    conv['frac_digits'], x), grouping=True)
    print(s)


def runAPI():
    # systemDef();
    # commandLine();
    stringRe();