# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib.parse import urlencode
import requests
import random
import json
import time


User_Agentlist = ["Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                  "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                  "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                  "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) ",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"]

base_url = 'https://www.lagou.com/jobs/positionAjax.json?'

headers = {
    "Host": "www.lagou.com",
    # "Origin": "https://www.lagou.com",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    "User-Agent": random.choice(User_Agentlist),
    # "X-Anit-Forge-Code": 0,
    # "X-Anit-Forge-Token": None,
    "X-Requested-With": "XMLHttpRequest",
}


def get_page(city, page):
    params = {
        'city': city,
        'needAddtionalResult': 'false'
    }
    url = base_url + urlencode(params)
    # print(url)
    # https://www.lagou.com/jobs/positionAjax.json?city=%E9%83%91%E5%B7%9E&needAddtionalResult=false
    if page == 1:
        formdata = {
            "first": 'true',
            "pn": page,
            "kd": "java"
        }
    else:
        formdata = {
            "first": 'false',
            "pn": page,
            "kd": "C++"
        }
    # print(formdata)

    try:
        response = requests.post(url, headers=headers, data=formdata)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('error:', e)


def write_to_file(filename, items):
    try:
        items = json.loads(items)
    except:
        text_list = []
    text_list = items['content']['positionResult']['result']
    with open(filename, 'a', encoding='utf-8') as f:
        for item in text_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    city_list = ['北京', '上海', '深圳', '广州', '成都',
                 '南京', '武汉', '西安', '郑州', '苏州', '天津']
    for city in city_list:
        for page in range(1, 31):
            items = get_page(city, page)
            write_to_file('C.txt', items)
            time.sleep(random.randint(1, 3))
    print('Finish')
