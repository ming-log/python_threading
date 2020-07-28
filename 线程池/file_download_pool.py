# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/28 14:32
import requests
import concurrent.futures as futures


def file_download(url, type='content'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    r = requests.get(url, headers=headers)
    if type == 'text':
        return r.text

    return r.content


class DownLoadExecutionerPool():
    def __init__(self):
        super().__init__()
        # 图片保存目录
        self.save_dir = './img_pool/'
        # 图片计数
        self.index = 0
        # 线程池, 最大线程30
        self.ex = futures.ThreadPoolExecutor(max_workers=30)

    """输入任务"""
    def put_task(self, urls):
        """
        :param urls: 线程作用的地址
        """
        if isinstance(urls, list):
            for url in urls:
                self.ex.submit(self.save_img, url)  # 作用函数为save_img, 传入参数url
        else:
            self.ex.submit(self.save_img, urls)

    """保存图片到本地"""
    def save_img(self, url):
        """
        :param url: 图片的url地址
        :return: 将图片保存到本地
        """
        content = file_download(url)
        # 截取图片名称
        index = url.rfind('/')
        file_name = url[index+1:]
        save_name = self.save_dir + file_name
        with open(save_name, 'wb+') as f:
            f.write(content)
            self.index += 1
            print(save_name + "下载成功!  当前已下载图片总数：" + str(self.index))



























