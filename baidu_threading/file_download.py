# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/28 10:31

import requests
import threading
from queue import Queue


def file_download(url, type='content'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    r = requests.get(url, headers=headers)
    if type == 'text':
        return r.text
    return r.content

class DownLoadExecutioner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.q = Queue(maxsize=50)
        # 图片保存目录
        self.save_dir = './img/'
        # 图片计数
        self.index = 0

    def put_task(self, urls):
        if isinstance(urls, list):
            for url in urls:
                self.q.put(url)
        else:
            self.q.put(urls)

    def run(self):
        while True:
            url = self.q.get()
            print(url)
            content = file_download(url)

            # 截取图片名称
            index = url.rfind('/')
            file_name = url[index+1:]
            save_name = self.save_dir + file_name
            with open(save_name, 'wb+') as f:
                f.write(content)
                self.index += 1
                print(save_name + "下载成功!  当前已下载图片总数：" + str(self.index))



























