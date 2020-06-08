# ！/usr/bin/env python
# -*- coding:utf8 -*-
import requests
import json
import re
import argparse
from tqdm import tqdm


class Spider:
    def __init__(self, url):
        self.host = url
        self.weight_list = {}
        self.status_code = 200
        self.response = ''
        self.text = ''

    def send_url(self, path):
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Connection": "keep-alive"
        }
        request = requests.get(url=self.host + path, headers=headers, allow_redirects=False)
        self.status_code = request.status_code
        self.response = request.headers
        self.text = request.text

    def check(self, rule):
        if (rule.get("contain") and self.text.find(rule.get("contain")) >= 0) or (
                rule.get("statuscode") and rule.get("statuscode") == self.status_code):
            if self.weight_list.get(rule.get("name")):
                self.weight_list.update({rule.get("name"): self.weight_list.get(rule.get("name")) + rule.get("weight")})
            else:
                self.weight_list.update({rule.get("name"): rule.get("weight")})
            if rule.get("print"):
                try:
                    print("[!]------------------------------------------",
                          re.compile(rule.get("print")).findall(self.text)[0])
                except Exception as e:
                    del e
                    print("[!]------------------------------------------", "print信息匹配错误", rule.get('path'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='scanWebFinger -u http://baidu.com')
    print("""
    ---------------------------------------
    |   Author:大耳朵图图                  
    |   >_<      0.0       +_+      /*_*/ 
    ---------------------------------------
    """)
    parser.add_argument('-u', "--url", type=str, required=True, help="需要识别的url,后面不需要加 / ")
    args = parser.parse_args()
    spider = Spider(url=args.url)
    with open("fingerprint.json", 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
    for e in tqdm(data, ncols=50):
        spider.send_url(path=e.get('path'))
        spider.check(rule=e)
        if spider.weight_list.get(e.get("name")) and spider.weight_list.get(e.get("name")) >= 90:
            break
    print("")
    for e in spider.weight_list:
        print("[+]------------------------------------------", "平台:[{}] 权重点:[{}]".format(e, spider.weight_list.get(e)))
    input("")
