import requests
import json
from fake_useragent import UserAgent
import time
import hashlib
import random

'''
有道翻译 http://fanyi.youdao.com/
'''


class YouDao(object):

    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.ua = UserAgent().random
        '''
        每次翻译cookie都发生了改变，最后___rl__test__cookies为当前时间戳
        '''
        self.headers = {
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http: // fanyi.youdao.com /',
            'User-Agent': self.ua,
            'Cookie': 'OUTFOX_SEARCH_USER_ID=1343573861@10.169.0.82; JSESSIONID=aaaPvXVSth-S5dKortRgx; OUTFOX_SEARCH_USER_ID_NCOO=1717349831.5539143; ___rl__test__cookies=' + str(int(time.time() * 1000))
        }

    def payload(self, before, lan):
        # 请求体改变的就ts,bv,sign,salt,i
        # ts为当前时间戳
        # bv为浏览器ua的hash值
        # i 为需要翻译的内容
        # salt 为时间戳 ＋ 10以内的随机整数
        # sign为 'fanyideskweb' + 翻译内容 + i + 'Nw(nmmbP%A-r6U3EUn]Aj'的hash值，可在fanyi.min.js中找到
        r = str(int(time.time() * 1000))
        i = r + str(int(random.random()*10))
        sign = hashlib.md5(("fanyideskweb" + before + i +
                            "Nw(nmmbP%A-r6U3EUn]Aj").encode('utf-8')).hexdigest()
        return {
            'i': before,
            'from': 'AUTO',
            'to': lan,
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': i,
            'sign': sign,
            'ts': r,
            'bv': hashlib.md5(self.ua.encode('utf-8')).hexdigest(),
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }

    def translate(self, before, lan):
        resp = requests.post(
            self.url, headers=self.headers, data=self.payload(before, lan))
        ret_dict = json.loads(resp.text)
        print(ret_dict)
        print(f'{before}')
        print(ret_dict['translateResult'][0][0]['tgt'])


if __name__ == "__main__":
    YouDao().translate('反反爬虫', 'en')
