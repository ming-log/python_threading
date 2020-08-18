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

"""
python的并发模块concurrent
Python3.2开始，标准库为我们提供了concurrent.futures模块，它提供了ThreadPoolExecutor和ProcessPoolExecutor两个类，
实现了对threading和multiprocessing的进一步抽象，对编写线程池/进程池提供了直接的支持,他属于上层的封装，
对于用户来说，不用在考虑那么多东西了。

1. Executor
Exectuor是基础模块，这是一个抽象类，其子类分为ThreadPoolExecutor和ProcessPoolExecutor，分别被用来创建线程池和进程池。
提供的方法如下：
1.1 Executor.submit(fn, *args, **kwargs)
    fn:为需要异步执行的函数
    args,kwargs:为给函数传递的参数
 
e.g.   
with ThreadPoolExecutor(max_workers=1) as executor:
future = executor.submit(pow, 323, 1235)
print(future.result())

1.2 Executor.map(fn, *args, **kwargs)
    map(func, *iterables, timeout=None)
    此map函数和python自带的map函数功能类似，只不过concurrent模块的map函数从迭代器获得参数后异步执行。
    并且，每一个异步操作，能用timeout参数来设置超时时间，timeout的值可以是int或float型，
    如果操作timeout的话，会raisesTimeoutError。如果timeout参数不指定的话，则不设置超时间。
    func：为需要异步执行的函数
    iterables：可以是一个能迭代的对象.
    timeout：设置每次异步操作的超时时间
  
e.g.       
from concurrent.futures import ThreadPoolExecutor
import requests
URLS = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
def load_url(url):
        req= requests.get(url, timeout=60)
        print('%r page is %d bytes' % (url, len(req.content)))
executor = ThreadPoolExecutor(max_workers=3)
executor.map(load_url,URLS)
print('主线程结束')

1.3 Executor.map(fn, *args, **kwargs)
    此函数用于释放异步执行操作后的系统资源。Executor实现了enter__和__exit使得其对象可以使用with操作符。
    在这里可以使用with上下文关键字代替，如上面第一个submit的例子。

2. Future对象
submit函数返回future对象，future提供了跟踪任务执行状态的方法,
Future实例可以被Executor.submit()方法创建。除了测试之外不应该直接创建。

cancel()：尝试去取消调用。如果调用当前正在执行，不能被取消。这个方法将返回False，否则调用将会被取消，方法将返回True
cancelled()：如果调用被成功取消返回True
running()：如果当前正在被执行不能被取消返回True
done()：如果调用被成功取消或者完成running返回True
result(Timeout = None)：拿到调用返回的结果。如果没有执行完毕就会去等待
exception(timeout=None)：捕获程序执行过程中的异常
add_done_callback(fn)：将fn绑定到future对象上。当future对象被取消或完成运行时，fn函数将会被调用

3. wait方法
wait方法接会返回一个tuple(元组)，tuple中包含两个set(集合)，一个是completed(已完成的)另外一个是uncompleted(未完成的)。
使用wait方法的一个优势就是获得更大的自由度，它接收三个参数FIRST_COMPLETED, FIRST_EXCEPTION 和ALL_COMPLETE，
默认设置为ALL_COMPLETED。


如果采用默认的ALL_COMPLETED，程序会阻塞直到线程池里面的所有任务都完成，再执行主线程：
#!/usr/bin/env python 
# encoding: utf-8 
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import requests
URLS = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
def load_url(url):
    req = requests.get(url, timeout=60)
    print('%r page is %d bytes' % (url, len(req.content)))
executor = ThreadPoolExecutor(max_workers=3)
f_list = []
for url in URLS:
    future = executor.submit(load_url,url)
    f_list.append(future)
print(wait(f_list))
print('主线程结束')


如果采用FIRST_COMPLETED参数，程序并不会等到线程池里面所有的任务都完成。
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import requests
URLS = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
def load_url(url):
    req=requests.get(url, timeout=60)
    print('%r page is %d bytes' % (url, len(req.content)))
executor = ThreadPoolExecutor(max_workers=3)
f_list = []
for url in URLS:
    future = executor.submit(load_url,url)
    f_list.append(future)
print(wait(f_list,return_when='FIRST_COMPLETED'))
print('主线程结束')
"""

























