# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/28 10:29

from lxml import etree
from file_download import DownLoadExecutioner, file_download


class XiaoHua:
    def __init__(self, init_url):
        self.init_url = init_url
        self.download_executioner = DownLoadExecutioner()

    def start(self):
        self.download_executioner.start()   ## 初始的queue没有值为什么直接运行这行，并且程序能执行
        self.download_img(self.init_url)

    def download_img(self, url):
        html_text = file_download(url, type='text')     # 下载页面
        html = etree.HTML(html_text)
        img_urls = html.xpath("//a[contains(@class,'thumbnail')]/img/@bpic")    # 查找该页面所有的图片链接
        self.download_executioner.put_task(img_urls)      # 将查找到的图片链接放入队列queue中

        # 获取下一页的链接
        next_page = html.xpath("//div[@id='frs_list_pager']/a[contains(@class,'next')]/@href")
        next_page = "http:" + next_page[0]   # 得到下一个页面的链接
        self.download_img(next_page)      # 循环重复进入下一页操作


if __name__ == '__main__':
    x = XiaoHua("http://tieba.baidu.com/f?kw=校花&ie=utf-8")
    x.start()


import threading,time
import queue
# 最多存入10个
q = queue.Queue(maxsize=10)
def producer(name):
    count = 1
    while True:
        #　生产一块骨头
        q.put("骨头 %s" % count )
        print("生产了骨头",count)
        count +=1
        time.sleep(0.3)
def consumer(name):
    while True:
        print("%s 取到[%s] 并且吃了它" %(name, q.get()))
        time.sleep(1)
        # 告知这个任务执行完了
        q.task_done()
# 生成线程
p = threading.Thread(target=producer,args=("德国骨科",))
c = threading.Thread(target=consumer,args=("陈狗二",))
d = threading.Thread(target=consumer,args=("吕特黑",))
# 执行线程
p.start()
c.start()
d.start()
