# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/28 14:31


import requests
from lxml import etree

from file_download_pool import DownLoadExecutionerPool, file_download


class XiaoHua:
    def __init__(self, init_url):
        self.init_url = init_url
        self.download_executioner = DownLoadExecutionerPool()

    def start(self):
        self.download_img(self.init_url)

    """调用put_task，往里面加入图片地址，开始下载任务"""
    def download_img(self, url):
        html_text = file_download(url, type='text')
        html = etree.HTML(html_text)
        img_urls = html.xpath("//a[contains(@class,'thumbnail')]/img/@bpic")
        self.download_executioner.put_task(img_urls)

        # 获取下一页的连接
        next_page = html.xpath("//div[@id='frs_list_pager']/a[contains(@class,'next')]/@href")
        next_page = "http:" + next_page[0]
        self.download_img(next_page)


if __name__ == '__main__':
    x = XiaoHua("http://tieba.baidu.com/f?kw=校花&ie=utf-8")
    x.start()



























