# -*- coding:utf-8  -*-
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed

# 文件读取
def read_pdf(pdf_name):
    # 以二进制读模式打开
    fp = open(pdf_name, 'rb')
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个pdf文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始密码，如果没有密码 就创建一个空的字符串
    doc.initialize('')
    # 检测文档是否提供txt转换，不提供就抛出异常
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    # 创建PDf 资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    list_read = [];
    # 循环遍历列表，每次处理一个page的内容
    bol=False;
    for i, page in enumerate(doc.get_pages(), 1):
        index = "===========《第{}页》===========".format(i)
        context_sent="";
        print(index)
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        for x in layout:
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox,
            # LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性
            if not isinstance(x, LTTextBoxHorizontal):
                continue
            results = x.get_text().split("\n");
            for i in range(len(results)):
                if(len(results[i])<=1):
                    continue;
                if(results[i][-1]=='-'):
                    results[i]=results[i][0:-1];
                else:
                    results[i] = results[i]+" ";

            results = ''.join(results);

            list_read.append(results);
    return list_read;
import requests
import re

def translated_content(text, target_language):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }
    # 请求url
    url = "https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2609060161424095358&bl=boq_translate-webserver_20201203.07_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=359373&rt=c"
    # 数据参数
    from_data = {
        "f.req": r"""[[["MkEWBc","[[\"{}\",\"auto\",\"{}\",true],[null]]",null,"generic"]]]""".format(text, target_language)
    }
    try:
        r = requests.post(url, headers=headers, data=from_data, timeout=60)
        if r.status_code == 200:
            # 正则匹配结果
            response = re.findall(r',\[\[\\"(.*?)\\",\[\\', r.text)
            if response:
                response = response[0]
            else:
                response = re.findall(r',\[\[\\"(.*?)\\"]', r.text)
                if response:
                    response = response[0]
            return response
    except Exception as e:
        print(e)
        return False
if __name__ == '__main__':
    name = "D:/贵州大学/CVPR/语义分割/2020/具有自校正网络的半监督语义图像分割.pdf";
    lsit_read = read_pdf(name)
    with open('具有自校正网络的半监督语义图像分割'+".txt", 'w', encoding='utf-8') as f:
        for i in lsit_read:
            trans = translated_content(i,'zh');
            print(trans)
            f.write(i+"\n"+trans+"\n");
    #print("总共消耗时间为:",time2-time1)