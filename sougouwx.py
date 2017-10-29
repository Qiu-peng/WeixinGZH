# -*- coding:utf-8 -*-

import requests
from lxml import etree
import json
import time
import random

page = 1
item_list = []


def start_work(name):
    start_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query='+str(name)+'&ie=utf8&_sug_=n&_sug_type_=&page='
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    # proxy_list = [
    #     {"http": "60.169.78.218:808"},
    #     {"http": "220.166.243.12:8118"},
    #     {"http": "110.73.9.247:8123"},
    #     {"http": "110.72.44.198:8123"},
    #     {"http": "123.185.129.186:8080"},
    #     {"http": "61.135.217.7:80"},
    #     {"http": "114.67.149.209:808"},
    #     {"http": "118.114.77.47:8080"}
    # ]
    # proxy = random.choice(proxy_list)
    proxy = {"https": "175.17.5.180:8080"}
    while True:
        # 发送url请求，返回html页面
        html = send_request(start_url, headers, proxy)

        if not html:
            break
        # 处理html页面
        load_page(html)

        content = json.dumps(item_list)
        with open("wenxin.json", "w") as f:
            f.write(content)


def send_request(url, headers, proxy):
    global page
    response = requests.get(url+str(page), headers=headers, proxies=proxy)
    html = response.content
    time.sleep(2)
    if page < 10:
        print("正在爬取第%d页..." % page)
        page += 1
    else:
        return False
    return html


def load_page(html):
    # 指定lxml解析器
    # print(html)
    html = etree.HTML(html)
    # print(html)
    # 取出每一页的所有结点
    node_list = html.xpath('//div[@class="txt-box"]')

    for node in node_list:
        item = {}
        item[u'wz_name'] = node.xpath('./p[@class="tit"]/a')[0].xpath("string(.)")
        # print(node.xpath('./p[@class="tit"]/a')[0].xpath("string(.)"))
        item[u'wz_url'] = node.xpath('./p[@class="tit"]/a/@href')[0]
        item[u'wz_zuoz'] = node.xpath('./p[@class="info"]')[0].xpath("string(.)")
        item_list.append(item)


if __name__ == '__main__':
    name = input("请输入要爬取的name：")
    start_work(name)


