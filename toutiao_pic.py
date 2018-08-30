# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from hashlib import md5
import requests
from urllib.parse import urlencode
from multiprocessing import Pool


def get_html(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:

            return response.json()
    except requests.ConnectionError:
        return None


def get_images(items):
    if items.get('data'):
        for item in items.get('data'):
            # print('item', item)
            title = item.get('title')
            # article_url = item.get('article_url')
            images = item.get('image_list')
            # print(images)
            for image in images:
                yield {
                    "image": 'http:' + image.get('url'),
                    "title": title
                }


def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = "{0}/{1}.{2}".format(item.get('title'),
                                             md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print('ok')
            else:
                print('Already exists', file_path)
    except requests.ConnectionError:
        print('Failed to save image')


def main(offset):
    items = get_html(offset)
    for item in get_images(items):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == "__main__":
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
