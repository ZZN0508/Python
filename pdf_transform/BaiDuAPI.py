# -*- coding:utf-8  -*-
import requests
import os
import execjs
import sys
import json
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
def get_post_data(query_string):  # 1.url，post_data
    arrRet=['','','','','']
    arrRet[0]=query_string
    os.environ["NODE_PATH"] = os.getcwd()+"/node_modules"
    inputData = query_string
    with open("./baidujs.js") as f:
        jsData = f.read()
    p = execjs.compile(jsData).call("e", inputData)
    #print(p)
    url = "https://fanyi.baidu.com/basetrans"
    data = {
        "from": "en",
        "to": "zh",
        "query": query_string,
        "transtype": "translang",
        "simple_means_flag": "3",
        "token": "f8c8ea6c95d6e9e7ba318e136ee2c490",
        "sign": p # 随着翻译内容变化而变化
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "Cookie": "BDUSS=I2N2tPRVBXZk5zQnZJdmV6QnY5ZDc1anNEU2lrcWVCN25lQ2t6bXJ2amd5a1JiQVFBQUFBJCQAAAAAAAAAAAEAAACiHXkweGllY2hlbmcxOTk1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA9HVvgPR1bcT; BIDUPSID=FCDC0DE1E2A0BC542BE845EF57F0DA5F; PSTM=1560475969; BAIDUID=FCDC0DE1E2A0BC54F756173A5902B1FB:FG=1; locale=zh; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1561467752,1561468730,1561469040,1561469241; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1561469241; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1561468730,1561469040,1561469241,1561470454; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1561470454; yjs_js_security_passport=5453d43730575af39e7a665570b61ece7f5fc95b_1561470456_js"
    }
    response = requests.post(url, data=data, headers=headers)
    try:
        temp_dict = json.loads(response.content.decode())['dict']
        print(temp_dict["symbols"][0]['parts'][0]['means'][0])
        global li
        arrRet[1]="/"+temp_dict["symbols"][0]["ph_en"]+"/ /"+""+temp_dict["symbols"][0]["ph_am"]+"/"
        li.append("/"+temp_dict["symbols"][0]["ph_en"]+"/ /"+""+temp_dict["symbols"][0]["ph_am"]+"/")
        arr=temp_dict["symbols"][0]['parts']
        for a in arr:
            s=str(a["part"])+str(a["means"]);
            arrRet[2]=arrRet[2]+s;
            li.append(s)
        print(li);
        if( 'tags' in temp_dict):
            s=temp_dict["tags"]["core"]
            li.append(s);
            arrRet[3]=s;
        else:
            arrRet[3]=' '
        url='https://fanyi.baidu.com/extendtrans'
        response = requests.post(url, data=data, headers=headers)
        arrs = json.loads(json.loads(response.content.decode())['data']['st'])
        strs=''
        for i in arrs:
            strs=strs+"["
            for j in i:
                if isinstance(j,list):
                    for k in j:
                        strs=strs+k[0]+" "
                    strs=strs+","
            strs=strs+"]"
        arrRet[4]=strs;
        li.append(strs+"\n")
        #print(','.join(str(s) for s in li))
    except BaseException as e:
        print(arrRet)
        #li=li+str(strs+"]")+"\n"
    finally:
        print('添加失败')
        # for l in li:
        #     print (l);
li=[];
if __name__ == '__main__':
   #li.append(query_string)
    query_string=['In this paper, we focus on fine-grained image-to-image']
    for i in query_string:
        get_post_data(i)

