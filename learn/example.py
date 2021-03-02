# -*- coding: utf-8 -*-
from decimal import *;

def number():
    # floor division -- 向下取整除法
    print(17 // 2);  # 8
    # 乘方 **优先权高与-顾如果计算-2的四次方需要提高-2的优先级
    print(2 ** 4);  # 16
    print(-2 ** 4);  # -16
    print((-2) ** 4);  # 16
    # Decimal对象
    r2 = Decimal(10) / Decimal(3)
    print("高精度", r2)  # 高精度 3.333333333333333333333333333
    print("普通", 10 / 3)  # 普通 3.3333333333333335
    # 设置decimal的精度,默认是28位
    # getcontext()返回活动线程当前上下文
    getcontext().prec = 30;  # 设置decimal的精度为30
    r2 = Decimal(10) / Decimal(3)
    print("高精度", r2)  # 高精度 3.33333333333333333333333333333
    print(Decimal('1012'));  # 1012,可以把字符串转为数字，如果是非数字字符串会报错
    print(Decimal('-Infinity'));  # -Infinity，如果字符串是Infinity ，-Infinity 和 NaN 的话可以输出
    print(Decimal(23) > 12)  # True
    print(Decimal('3.5') < 3.7)  # True
    # 当设置比较运算中不允许 float 和 Decimal 混合时,即开启 FloatOperation
    # traps设置异常是否开启捕获
    getcontext().traps[FloatOperation] = True
    # print(Decimal('3.5') < 3.7)#报错
    print(Decimal('3') < 3)  # False
    getcontext().traps[FloatOperation] = False;
    # Decimal(0表示正数1表示负数,(元祖)，整数指数)
    print(Decimal((0, (1, 4, 1, 4), -2)));  # 0表示正数，-2表示1414*10^-2=14.14
    # 返回给定数字的最简分数
    print(Decimal('-12.5').as_integer_ratio());
    # 比较两个Decimal实例的值，大于返回1，相等返回0小于返回-1，其中一个为NaN则返回NaN
    print(Decimal(12).compare(Decimal(34)));
    # 返回参数的绝对值
    print(Decimal('-34').copy_abs());  # 34
    # 返回参数的相反数
    print(Decimal('34').copy_negate());  # -34
    # 返回第一个操作数的副本，其符号设置为与第二个操作数的符号相同
    print(Decimal('2.3').copy_sign(Decimal('-1.5')))  # -2.3
    # 返回给定数字的（自然）指数函数``e**x``的值。
    print(Decimal('1').exp());  # e^1
    # 判断参数是否是一个有限的数，如果参数是一个有限的数，则返回为 True ；如果参数为无穷大或 NaN ，则返回为 False。
    print((Decimal('3.3453453') / Decimal('3')).is_finite());  # True
    print(Decimal('NaN').is_finite());  # Fale
    # 判断参数是否为无穷大，如果参数为正负无穷大，则返回为 True ，否则为 False 。
    print(Decimal('Infinity').is_infinite());  # True
    # 判断是否为空。如果参数为 NaN （无论是否静默），则返回为 True ，否则为 False 。
    print(Decimal('12').is_nan());  # False
    # 判断参数是否带有负号，如果参数带有负号，则返回为 True，否则返回 False。注意，0 和 NaN 都可带有符号
    print(Decimal('12').is_signed());  # False
    # 判断参数是否为0如果参数是0（正负皆可），则返回 True，否则返回 False。
    print(Decimal('0').is_zero());  # True
    # 返回操作数的自然对数（以 e 为底）
    print(Decimal('2').ln());  # In2=0.693147180559945309417232121458
    # 返回操作数的以十为底的对数
    print(Decimal('100').log10());  # lg100=2
    # 转换为字符串
    print(Decimal('100').to_eng_string() + "ad")

def string():
    print('C:\some\name');
    # 如果不希望前置了\的字符转义成特殊字符，可以使用 原始字符串 方式，在引号前添加 r 即可
    print(r'C:\some\name');
    # 字符串字面值可以跨行连续输入。一种方式是用三重引号："""...""" 或 '''...'''。字符串中的回车换行会自动包含到字符串中，如果不想包含，在行尾添加一个 \ 即可
    print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")
    # 字符串可以用 + 进行连接（粘到一起），也可以用 * 进行重复
    print(3 * 'un' + 'ium');  # 复制3次un再与ium拼接
    # 相邻的两个或多个 字符串字面值 （引号引起来的字符）将会自动连接到一起.
    # 只能对字面值这样操作，变量或表达式不行:
    print('第一个' '第二个' '第三个');  # 第一个第二个第三个
    # 字符串索引，第一个字符索引是 0，索引也可以用负数，这种会从右边开始数
    word = "hello word";
    print(word[0] + '--' + word[3] + '--' + word[-1] + '--' + word[-3]);  # h--l--d--o
    # 字符串还支持 切片索引可以得到单个字符，而 切片 可以获取子字符串:
    print(word[0:-3]);  # hello w,包含索引为0的不包含索引为-3的
    # 如果从索引为0开始可以省略开始索引s[:i]
    print(word[:-3]);  # hello w
    # 省略结束索引时默认为到字符串的结束s[i:]
    print(word[4:]);  # o word
    # Python 中的字符串不能被修改，它们是 immutable 的。因此，向字符串的某个索引位置赋值会产生一个错误
    # str.capitalize()返回原字符串的副本，其首个字符大写，其余为小写。
    print("abcdAe".capitalize());  # Abcdae
    # str.casefold()消除大小写类似于转为小写，但是更加彻底一些，因为它会移除字符串中的所有大小写变化形式
    print("AbcdgEFdgdsß".casefold());  # abcdgefdgdsss,会把法语ß转为ss
    # str.lower()转小写，但是只转换英文字母
    print("AbcdgEFdgdsß".lower());  # abcdgefdgdsß
    # str.center(width(返回字符串长度)[filchar(填充内容)])
    # width为数字，fillchar为ASCII中内容
    # 如果width小于原字符串长度则返回原字符串,如果width长度大于原字符串长度则填充fillchar，如果fillchar为空则补充空格
    print("abc".center(6));
    print("abc".center(6, '1'));
    print("abc".center(1));
    """ str.count(sub[, start[, end]])
        sub -- 搜索的子字符串
        start -- 字符串开始搜索的位置。默认为第一个字符,第一个字符索引值为0。
        end -- 字符串中结束搜索的位置。字符中第一个字符的索引为 0。默认为字符串的最后一个位置。
    该方法返回子字符串在字符串中出现的次数。"""
    print("ababaabcdabcds".count("ab"))  # 4
    print("ababaabcdabcds".count("abfdg"[0:2]))  # 4，判断ab出现的次数
    # str.encode(encoding="utf-8", errors="strict")
    # 修改字符串的编码格式并返回编码后的字符串。errors是设置不同错误的处理方案。默认为 'strict',意为编码错误引起一个UnicodeError。 其他可能得值有 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace' 以及通过 codecs.register_error() 注册的任何值。
    print("这是个编码".encode("gbk"));  # 转换为gbk
    # str.endswith(suffix[, start[, end]])
    # 如果字符串以指定的 suffix 结束返回 True，否则返回 False。如果有可选项 start，将从所指定位置开始检查。 如果有可选项 end，将在所指定位置停止比较
    print("fdgsgdsd123".endswith('123456'[0:3]));  # True;是判断结尾是否是123
    # str.expandtabs(tabsize=8)
    # 把字符串中的 tab 符号 \t 转为空格，tab 符号 \t 默认的空格数是 8，在第 0、8、16...等处给出制表符位置，如果当前位置到开始位置或上一个制表符位置的字符数不足 8 的倍数则以空格代替。
    # tabsize -- 指定转换字符串中的 tab 符号('\t')转为空格的字符数。
    print("fdsf\nfdf\tfsdfsd\rfdsf".expandtabs())
    # str.find(sub[, start[, end]])
    # 方法检测字符串中是否包含子字符串 str ，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则返回-1
    print("fsdfasdg".find('fs'));  # 0
    print("fsdfasdg".find('as', 1, 5));  # -1,是在sdfa中查找as
    # str.format(*args, **kwargs);执行字符串格式化操作
    print("1+2={0},2*2={1}".format(1 + 2, 2 * 2));
    # str.format_map(mapping)
    # 与format没什么区别，只是format_map的值为map集合
    dicts = {'name': '张三', 'age': 23};
    print('name is {name},age is {age}'.format_map(dicts))
    # str.index(sub[, start[, end]])
    # 方法检测字符串中是否包含子字符串 str ，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则报ValueError错误
    print("fsdfasdg".index('fs'));  # 0
    # print("fsdfasdg".index('as',1,5));#抛出异常,是在sdfa中查找as
    # str.isalnum()
    # 如果字符串中的所有字符都是字母数字，并且至少有一个字符，则返回True，否则返回False。
    print('fdsfd1234'.isalnum());  # True
    print('fdsfd12|34'.isalnum());  # False
    # str.isalpha()
    # 如果字符串中的所有字符都是字母，并且至少有一个字符，则返回True，否则返回False。
    print('fdsfd1234'.isalpha());  # False
    print('fdsfd'.isalpha());  # True
    # str.isascii()
    # 如果字符串为空或字符串中的所有字符为ASCII，则返回True，否则返回False
    print('fdsfd1234'.isascii());  # True
    print('fds和fd'.isascii());  # False
    # str.isdecimal()
    # 如果字符串中的所有字符都是十进制字符，并且至少有一个字符，则返回True，否则返回False。如U+0660，阿拉伯-印度数字零
    print("\u096a".isdecimal());  # True,\u096a是印度数字5
    #str.isdigit()
    #如果字符串中的所有字符都是数字并且至少有一个字符，则返回True，否则返回False。数字包括十进制字符和需要特殊处理的数字，如兼容性上标数字。
    print('4'.isdigit());#True
    print('四'.isdigit());#False
    print('④'.isdigit());#True
    print('1/4'.isdigit());#False
    #str.isidentifier()
    #如果字符串是一个标识符或者关键字返回True，否则返回False
    print("false".isidentifier());#True
    #str.islower()
    #判断字符串中字母是否是小写字母
    print("fdfdg12fdg".islower());#True
    print("fdfdg12Fdg".islower());#False
    #str.isnumeric()
    #如果字符串中的所有字符都是数字字符，并且至少有一个字符，则返回True，否则返回False。数字字符包括数字字符和所有具有Unicode数值属性的字符，例如U+2155，普通分数1 / 5。
    print('4'.isnumeric());#True
    print('四'.isnumeric());#True
    print('④'.isnumeric());#True
    print('1/4'.isnumeric());#False
    #str.isprintable()
    #如果字符串中的所有字符都可打印，或者字符串为空，则返回True，否则返回False。非打印字符是指在Unicode字符数据库中定义为“Other”或“Separator”的字符，除了被认为是可打印的ASCII空间(0x20)之外。
    print("fdfd".isprintable());#True
    print("fdgdf\tdsfds\n".isprintable());#False
    #str.isspace()
    #检测字符串是否只由空格组成，是则返回True，否则返回False。
    print(' fdf dfs dfd'.isspace());#False
    print('   '.isspace());#True
    #str.istitle()
    #检测字符串中所有的单词拼写首字母是否为大写，且其他字母为小写
    print('Fsfdf'.istitle());#True
    print('FsfdfF'.istitle());#False
    print('Fsfdf1和'.istitle());#True
    print('1Fsfdf1和'.istitle());#True
    print('Fsf1df'.istitle());#False，1在字母中间
    #str.isupper()
    #检测字符串中所有的字母是否都为大写。
    print('FFF'.isupper());#True
    print('FFFf'.isupper());#False
    print('FFF1'.isupper());#True
    print('FF1F'.isupper());#True
    print('1FFF2'.isupper());#True，1在字母中间
    #str.join(iterable)
    #将序列中的元素以iterable指定的字符连接生成一个新的字符串
    print('-'.join(['2','3','4']));#2-3-4
    #str.ljust(width[, fillchar])
    #返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串。如果指定的长度小于原字符串的长度则返回原字符串。
    print('dfsdf'.ljust(3));#dfsdf;
    print('dfsdf'.ljust(8));#dfsdf        ;
    print('dfsdf'.ljust(8,'-'));#dfsdf---;
    # str.lstrip([chars])
    #用于截掉字符串左边的空格或指定字符。 chars 参数为指定要移除字符的字符串。 如果省略或为 None，则 chars 参数默认移除空格符。 实际上 chars 参数并非指定单个前缀；而是会移除参数值的所有组合
    print('  dfdDF'.lstrip());#dfdDF
    print('222dfdDF2222'.lstrip('2'));#dfdDF2222
    # static str.maketrans(x[, y[, z]])
    #此静态方法返回一个可供 str.translate() 使用的转换对照表
    #创建字符映射的转换表，对于接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标
    trantab = str.maketrans('aeiou', '12345');
    #str.translate(table)
    #根据参数table给出的表(包含 256 个字符)转换字符串的字符,table翻译表，翻译表是通过maketrans方法转换而来
    print ("this is string example....wow!!!".translate(trantab))
    #str.partition(sep)
    #在 sep 首次出现的位置拆分字符串，返回一个 3 元组，其中包含分隔符之前的部分、分隔符本身，以及分隔符之后的部分。 如果分隔符未找到，则返回的 3 元组中包含字符本身以及两个空字符串。
    print('this1isstring1example'.partition('1'));
    #str.replace(old, new[, count])
    #返回字符串的副本，其中出现的所有子字符串 old 都将被替换为 new。 如果给出了可选参数 count，则只替换前 count 次出现。
    print('123-123-123-123-123'.replace('123','0',3))#0-0-0-123-123
    #str.rfind(sub[, start[, end]])
    #返回字符串最后一次出现的位置(从右向左查询)，如果没有匹配项则返回-1。
    print("this is really".rfind('is'));#5
    print("this is really".rfind('is',0,10));#5
    print("this is really".rfind('is',10,18));#-1
    print("this is really".rfind('is',0,5));#2
    # str.rindex(sub[, start[, end]])
    #类似于 rfind()，但在子字符串 sub 未找到时会引发 ValueError。
    print("this is really".rindex('is'));#5
    print("this is really".rindex('is',0,10));#5
    #print("this is really".rindex('is',10,18));#报错
    print("this is really".rindex('is',0,5));#2
    #str.rjust(width[, fillchar])
    #返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串。
    print( "this is string".rjust(20, '0'));#000000this is string
    print( "this is string".rjust(20));#      this is string
    #str.rpartition(sep)
    #在 sep 最后一次出现的位置拆分字符串，返回一个 3 元组，其中包含分隔符之前的部分、分隔符本身，以及分隔符之后的部分。 如果分隔符未找到，则返回的 3 元组中包含两个空字符串以及字符串本身。
    print('123-456--34'.rpartition('-'));#('123-456-', '-', '34')
    #str.rsplit(sep=None, maxsplit=-1)
    #返回一个由字符串内单词组成的列表，使用 sep 作为分隔字符串。 如果给出了 maxsplit，则最多进行 maxsplit 次拆分，从 最右边 开始。 如果 sep 未指定或为 None，任何空白字符串都会被作为分隔符
    print('123-456--34'.rsplit('-'));#['123', '456', '', '34']
    print('123-456--34'.rsplit('-',2));#['123-456', '', '34']
    #str.rstrip([chars])
    #返回原字符串的副本，移除其中的末尾字符。 chars 参数为指定要移除字符的字符串。 如果省略或为 None，则 chars 参数默认移除空格符。
    print('mississippi'.rstrip('ip9'));#mississ
    print('mississippi  '.rstrip());#mississippi;
    # str.split(sep=None, maxsplit=-1)
    #返回一个由字符串内单词组成的列表，使用 sep 作为分隔字符串。 如果给出了 maxsplit，则最多进行 maxsplit 次拆分
    print('123-345-5454--4545'.split('-'));#['123', '345', '5454', '', '4545']
    print('123-345-5454--4545'.split('-',2));#['123', '345', '5454--4545']
    #str.splitlines([keepends])
    #通过下述的转义符进行分割
    #\n,\r,\r\n,\v 或 \x0b,\f 或 \x0c,\x1c,\x1d,\x1e,\x85,\u2028,\u2029
    print('23\tfd\rfd\vdfs\fff'.splitlines());
    # str.startswith(prefix[, start[, end]])
    #如果字符串以指定的 prefix 开始则返回 True，否则返回 False
    print('1354'.startswith('13'));#True
    print('1354'.startswith('2'));#False
    print('1354'.startswith('13',0,3));#True
    print('1354'.startswith('13',1,2));#False
    #str.strip([chars])
    #返回原字符串的副本，移除其中的前导和末尾字符。 chars 参数为指定要移除字符的字符串。 如果省略或为 None，则 chars 参数默认移除空格符。
    print('123sdfdf123dsfds123'.strip('123'));#sdfdf123dsfds
    # str.swapcase()
    #返回原字符串的副本，其中大写字符转换为小写，反之亦然
    print('FddfsdfFdfsdfFdfs'.swapcase());#fDDFSDFfDFSDFfDFS
    # str.title()
    #返回原字符串的标题版本，其中每个单词第一个字母为大写，其余字母为小写
    print('I am people'.title());#I Am People
    # str.upper()
    #返回原字符串的副本，其中所有区分大小写的字符 4 均转换为大写。
    print('abcdefGHIGK'.upper());#ABCDEFGHIGK
    #str.zfill(width)
    #方法返回指定长度的字符串，原字符串右对齐，前面填充0
    print('dfd'.zfill(3));#dfd
    print('dfd'.zfill(6));#000dfd
    #对于 format % values (其中 format 为一个字符串)，在 format 中的 % 转换标记符将被替换为零个或多个 values 条目
    #s代表字符串，03d代表数字
    print('name is %(name)s age is %(age)03d.'%{'name': "张三", "age": 2});#name is 张三 age is 002.

def bytesDef():
    # 表示 bytes 字面值的语法与字符串字面值的大致相同，只是添加了一个 b 前缀
    # 单引号: b'同样允许嵌入 "双" 引号'。
    # 双引号: b"同样允许嵌入 '单' 引号"。
    # 三重引号: b'''三重单引号''', b"""三重双引号"""
    # bytes 字面值中只允许 ASCII 字符（无论源代码声明的编码为何）。 任何超出 127 的二进制值必须使用相应的转义序列形式加入 bytes 字面值。

    #bytes.fromhex(string);
    #用来将hexstr导入bytes对象，相当于用hexstr来创建bytes对象
    print(bytes.fromhex('2Ef0 F1f2  '));#b'.\xf0\xf1\xf2'
    #bytes.hex()
    #返回一个字符串对象，该对象包含实例中每个字节的两个十六进制数字
    print(b'.\xf0\xf1\xf2'.hex());#2ef0f1f2

def bytearrayDef():
    # bytearray 对象没有专属的字面值语法，它们总是通过调用构造器来创建
    # 创建一个空实例:
    print(bytearray());# bytearray(b'')
    # 创建一个指定长度的以零值填充的实例:
    print(bytearray(3));#bytearray(b'\x00\x00\x00')
    # 通过由整数组成的可迭代对象:
    print(bytearray(range(3)));# bytearray(b'\x00\x01\x02')
    # 通过缓冲区协议复制现有的二进制数据: bytearray(b'Hi!')
    print(bytearray(b'Hi!'));# bytearray(b'Hi!')
    # bytearray.fromhex(value)
    # 返回一个解码给定字符串的 bytearray 对象。
    # VALUE内容必须是16进制内容，如果16进制能转化为ASCII则输出ASCII内容，如果无法转换直接输出对应的16进制内容
    # \xf0等价于0xf0
    print(bytearray.fromhex('2Ef0 F1f2  '));# bytearray(b'.\xf0\xf1\xf2')
    # bytearray(value).hex()
    # 将value十六进制转换为十进制
    print(bytearray(b'\xf0\xf1\xf2').hex());# f0f1f2
    # 由于 bytearray 对象是由整数构成的序列（类似于列表），因此对于一个 bytearray 对象 b，b[0] 将为一个整数，而 b[0:1] 将为一个长度为 1 的 bytearray 对象。
    # bytearray和str一样，方法也一样，只不过str直接"123"，而bytea需要b"123"

def listDef():
    #其中最常用的 列表 ，可以通过方括号括起、逗号分隔的一组值（元素）得到。一个 列表 可以包含不同类型的元素
    squares = ['a', 1, '-', b'2', 'c']
    print(squares);
    #list的索引和切片与字符串一样
    #list的内容修改方式,
    squares[1]=10;
    print(squares);
    squares[1:2]=[3];
    print(squares);
    #list内容插入
    squares.append(7**3);# append在末尾添加一次只能添加一种类型
    print(squares);
    squares[2:3]=[squares[2],4,5,6];# ['a', 3, '-', 4, 5, 6, b'2', 'c', 343] 在 索引为2处添加4,5,6
    print(squares);
    # 获取列表的长度
    print(len(squares));# 9
    # 列表的嵌套,相当于二维数组
    arraysList=[[1,2,3],[12,23,34],[23,34,45]];
    print(arraysList[0][1]);#2
    arraysList.append([56,67,78]);# 不可以arraysList[3]
    print(arraysList)

    lists=[1,2,3];
    #  list.append(x)
    # 在列表的末尾添加一个元素。相当于 a[len(a):] = [x] 。
    lists.append(4)
    print(lists);# [1, 2, 3, 4]
    # list.extend(iterable)
    # 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）'
    lists.extend([1,2]);
    print(lists)# [1, 2, 3, 4, 1, 2]
    # list.insert(i, x)
    # 在给定的位置插入一个元素。第一个参数是要插入的元素的索引,第二个参数是要插入的内容
    lists.insert(0,0);
    print(lists);# [0, 1, 2, 3, 4, 1, 2]
    #  list.remove(x)
    # 移除列表中第一个值为 x 的元素。如果没有这样的元素，则抛出 ValueError 异常
    lists.remove(1);
    print(lists);# [0, 2, 3, 4, 1, 2]
    # list.pop([i])
    # 删除列表中给定位置的元素并返回它。如果没有给定位置，a.pop() 将会删除并返回列表中的最后一个元素
    lists.pop(2);
    print(lists);# [0, 2, 4, 1, 2]
    lists.pop();
    print(lists);# [0, 2, 4, 1]
    # list.clear()
    # 移除列表中的所有元素。等价于``del a[:]``
    lists.clear();
    print(lists);# []
    lists=[1,2,3,1];
    # list.index(x[, start[, end]])
    # 返回列表中第一个值为 x 的元素的从零开始的索引。如果没有这样的元素将会抛出 ValueError 异常。可选参数 start 和 end 是切片符号，用于将搜索限制为列表的特定子序列。返回的索引是相对于整个序列的开始计算的，而不是 start 参数。
    print(lists.index(1,1,len(lists)));# 3
    # list.count(x)
    # 返回元素 x 在列表中出现的次数。
    print(lists.count(1));# 2
    # list.sort(key=None, reverse=False)
    # 用于对原列表进行排序，如果指定参数，则使用比较函数指定的比较函数
    # key -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序
    # reverse -- 排序规则，reverse = True 降序， reverse = False 升序（默认）。
    lists.sort(reverse=True);
    print(lists);# [3, 2, 1, 1]
    # list.reverse()
    # 翻转列表中的元素。
    lists.reverse();
    print(lists);# [1, 1, 2, 3]
    # list.copy()
    # 返回列表的一个浅拷贝，等价于 a[:]。
    listCopy=lists.copy();
    print(id(listCopy)==id(lists));# False
    # 列表作为栈使用
    stack = [3, 4, 5]
    stack.append(6)
    stack.append(7)
    print(stack);# [3, 4, 5, 6, 7]
    stack.pop()
    print(stack);# [3, 4, 5, 6]
    stack.pop()
    stack.pop()
    print(stack);# [3, 4]
    # 列表作为队列使用
    # collections.deque是一个双向队列
    from collections import deque
    queue = deque(["Eric", "John", "Michael"])
    queue.append("Terry")
    queue.append("Graham")
    print(list(queue));# ['Eric', 'John', 'Michael', 'Terry', 'Graham']
    queue.popleft()
    print(list(queue));# ['John', 'Michael', 'Terry', 'Graham']
    queue.pop()
    print(list(queue));# ['John', 'Michael', 'Terry']
    # del语句
    # 从列表按照给定的索引而不是值来移除一个元素， del 语句也可以用来从列表中移除切片或者清空整个列表
    print(lists);# [1, 1, 2, 3]
    del lists[0];
    print(lists);# [1, 2, 3]
    del lists[0:1];
    print(lists);# [2, 3]
    del lists[:];
    print(lists);# []
    del lists;# 删除lists的内容

def control():
    #if语句
    x=34;
    if x < 0:
        x = 0
        print('Negative changed to zero')
    elif x == 0:
        print('Zero')
    elif x == 1:
        print('Single')
    else:
        print('More')
    #for 语句
    words = ['cat', 'window', 'defenestrate']
    for w in words:#cat 3  window 6  defenestrate 12
        print(w, len(w))
    #range(start, stop[, step])
    #start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）;
    #stop: 计数到 stop 结束，但不包括 stop。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5
    # step：步长，默认为1。例如：range（0， 5） 等价于 range(0, 5, 1)
    for i in range(5): # 0 1 2 3 4
        print(i)
    print(list(range(5,10)));# [5, 6, 7, 8, 9]
    print(list(range(0,10,3)));# [0, 3, 6, 9]
    print(list(range(0, -10, -3)));# [0, -3, -6, -9]
    #pass语言
    #pass 是空语句，是为了保持程序结构的完整性。pass 不做任何事情，一般用做占位语句
    s=0;
    while(s>0):
        pass;

# 函数定义 def 函数名( [参数1,参数2,参数3...])
# 函数参数可以设置默认值 def moren(a=1,b='sd',c=[]);设置默认值得参数为可选参数，如果给默认参数传参写法：s=value
# 对于默认参数是[]时，如果给list添加了值，则以后再调用时list不在是[]而是之前添加内容后的list
def f(a, L=[]):
    L.append(a)
    return L
# 函数中关键字参数
# 在函数调用中，关键字参数必须跟随在位置参数的后面
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print(action, voltage,type,state)
# 函数参数 *name与**name
# *name 必须出现在 **name 之前,*name接收元祖，**name接收dict
def cheeseshop(kind, *arguments, **keywords):
    print(kind);
    print(arguments);
    print(keywords);
# 可以用 lambda 关键字来创建一个小的匿名函数。
#调用此函数时会通过lambda表达式来返回一个函数,而且返回函数具有两个参数是x，y，计算y*x+n
def make_incrementor(n):
    return lambda x,y: y*x + n;
# 使用lambda来指定按照那个元素排序
def sortLambda(lists:list,i:int):
    lists.sort(key=lambda pair:pair[i]);
    return lists;
def tupleDef():
    t= 123,456,'hello';
    print(t);# (123, 456, 'hello')
    print(t[0]);# 123
    # t[0]=23;# 会报错，因为元组是不可变的
def setDef():
    basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
    print(basket);# {'orange', 'pear', 'apple', 'banana'}
    print('orange' in basket);# True
    print('crabgrass' in basket);# False
    a = set('abracadabra')# {'a', 'd', 'b', 'c', 'r'}
    b = set('alacazam')# {'a', 'l', 'c', 'z', 'm'}
    print(a);# {'a', 'd', 'b', 'c', 'r'}
    print(a - b);# {'d', 'r', 'b'}
    print(a | b);# {'z', 'b', 'd', 'l', 'm', 'a', 'c', 'r'}
    print(a & b);# {'c', 'a'}
    print(a ^ b);# {'l', 'm', 'z', 'b', 'd', 'r'}

def dictDef():
    tel = {'jack': 4098, 'sape': 4139}
    tel['guido'] = 4127
    print(tel);# {'jack': 4098, 'sape': 4139, 'guido': 4127}
    print(tel['jack']);# 4098
    del tel['sape']
    tel['irv'] = 4127
    print(tel);# {'jack': 4098, 'guido': 4127, 'irv': 4127}
    print(list(tel));# ['jack', 'guido', 'irv']
    print(sorted(tel));# ['guido', 'irv', 'jack']
    print('guido' in tel);# True
    print('jack' not in tel);# False
    # dict() 构造函数可以直接从键值对序列里创建字典。
    s=dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
    print(s);# {'sape': 4139, 'guido': 4127, 'jack': 4098}
    # 字典推导式可以从任意的键值表达式中创建字典
    s={x: x**2 for x in (2, 4, 6)}
    print(s);# {2: 4, 4: 16, 6: 36}
    # 当关键字是简单字符串时，有时直接通过关键字参数来指定键值对更方便
    s=dict(sape=4139, guido=4127, jack=4098);
    print(s)# {'sape': 4139, 'guido': 4127, 'jack': 4098}
    # 字典循环
    for k, v in s.items():
        print(k, v) # sape 4139
    # 当在序列中循环时，用 enumerate() 函数可以将索引位置和其对应的值同时取出
    for i, v in enumerate(['tic', 'tac', 'toe']):
        print(i, v); # 0 tic
    # 当同时在两个或更多序列中循环时，可以用 zip() 函数将其内元素一一匹配
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    for q, a in zip(questions, answers):
        print('What is your {0}?  It is {1}.'.format(q, a));# What is your name?  It is lancelot.
    # 如果要逆向循环一个序列，可以先正向定位序列，然后调用 reversed() 函数
    for i in reversed(range(1, 10, 2)):
        print(i);# 9 7 5 3 1
    # 如果要按某个指定顺序循环一个序列，可以用 sorted() 函数，它可以在不改动原序列的基础上返回一个新的排好序的序列
    basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
    for f in sorted(set(basket)):
        print(f);# apple banana orange pear
def printDef():
    # 使用格式化字符串字面值
    # 在字符串的开始引号或三引号之前加上一个 f 或 F.在 { 和 } 字符之间写可以引用的变量或字面值
    year = 2016
    event = 'Referendum'
    print(f'Results of the {year} {event}');# Results of the 2016 Referendum
    # 字符串的 str.format()
    # 需要更多的手动操作。你仍将使用 { 和 } 来标记变量将被替换的位置，并且可以提供详细的格式化指令，但你还需要提供要格式化的信息
    yes_votes = 42_572_654
    no_votes = 43_132_495
    percentage = yes_votes / (yes_votes + no_votes)
    #{:-9}表示占9位，但是yes_votes是8位在前面补空格，如果占位数小于实际位数原样输出
    print('{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage));
    # str(),repr();
    s = 'Hello, world.';
    print(str(s));# Hello, world.
    print(repr(s));# 'Hello, world.'
    print(str(1/7));# 0.14285714285714285
    x = 10 * 3.25
    y = 200 * 200
    s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
    print(s);# The value of x is 32.5, and y is 40000...
    # The repr() of a string adds string quotes and backslashes:
    hello = 'hello, world\n'
    hellos = repr(hello)
    print(hellos)# 'hello, world\n'
    # The argument to repr() may be any Python object:
    print(repr((x, y, ('spam', 'eggs'))));# (32.5, 40000, ('spam', 'eggs'))
    # 字典通过格式化遍历
    table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
    print('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
          'Dcab: {0[Dcab]:d}'.format(table))
    print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))

def writeDef():
    #open(name[, mode[, buffering]])
    #用于打开一个文件，创建一个 file 对象，相关的方法才可以调用它进行读写
    f = open('test.txt','r');
    with f:
        read_data=f.read();
        print(read_data);
    print(f.closed);# True 判断文件是否关闭
    f = open('test.txt','w');
    print(f.tell());
    f.write("hhhhhhhh");
    #f.tell()
    #返回一个整数,表示当前文件指针的位置(就是到文件头的字节数)。
    print(f.tell());
    f.seek(4,0); # 以文件头为准让光标移动4个单位
    f.write("ppppppp");
    f.close();

def jsonDef():
    import json
    # json.dumps();
    #将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
    dict1 = {"age": "12"}
    json_info = json.dumps(dict1)
    print("dict1的类型："+str(type(dict1)))
    print("通过json.dumps()函数处理：")
    print("json_info的类型："+str(type(json_info)))
    #json.loads()
    #json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
    dict1 = json.loads(json_info)
    print("json_info的类型："+str(type(json_info)))
    print("通过json.dumps()函数处理：")
    print("dict1的类型："+str(type(dict1)))
    # json.dump()
    # 函数的使用，将json信息写进文件
    json_info = "{'age': '12'}"
    file = open('1.json','w',encoding='utf-8')
    json.dump(json_info,file)
    # json.load()
    # 函数的使用，将读取json信息
    file = open('1.json','r',encoding='utf-8')
    info = json.load(file)
    print(info)
    
class CalcErorr(Exception):
    pass
class NumErorr(CalcErorr):
    def __init__(self,numA,numB):
        self.numA=numA
        self.numB=numB
    def __str__(self):
        return f"本计算器只接收整数!"
def calculator(a,b):
    try:
        if type(a)!=int or type(b)!=int:
            raise NumErorr(a,b)
    except Exception as e:
        print(e)
    else:
        c=a+b
        return c
def run():
    calculator(1.2,2)
    # jsonDef();
    # writeDef();
    # number();
    # string();
    # bytesDef();
    # listDef();
    # control();
    # print(f(1));# [1]
    # print(f(2));# [1, 2]
    # print(f(3));# [1, 2, 3]
    # parrot(voltage=1000000, action='VOOOOOM')
    # parrot({"voltage":1000000,"state":"dd", "action": "VOOOOOM","type":"dd"})
    # cheeseshop("Limburger", "It's very runny, sir.",
    #            "It's really very, VERY runny, sir.",
    #            shopkeeper="Michael Palin",
    #            client="John Cleese",
    #            sketch="Cheese Shop Sketch");
    # f=make_incrementor(30);
    # print(f(1,2));# 32
    # print((f(0,2)));# 30
    # s=sortLambda([('name1',23),('name2',26),('name3',24)],1); # [('name1', 23), ('name3', 24), ('name2', 26)]
    # print(s);
    # tupleDef();
    # setDef();
    # dictDef();
    # printDef();
