#__author__:"Ming Luo"
#date:2020/7/27

import threading
import time
from queue import Queue


def thread_job():
    print("T1 start")
    for i in range(10):
        time.sleep(0.1)
    print("T1 finsh")


def T2_job():
    print("T2 start")
    print("T2 end")


def main():
    # 创建一个线程他的工作是thread_job, 线程的名字是T1
    added_thread = threading.Thread(target=thread_job, name='T1')
    thread2 = threading.Thread(target=T2_job, name='T2')
    # 线程开始工作
    added_thread.start()
    thread2.start()
    # 运行join后面的命令，要等join上面的命令运行完
    added_thread.join()
    thread2.join()

    print("all done")

if __name__ == '__main__':
    main()


# 线程没有返回值，通过Queue进行存储
def job(l, q):
    for i in range(len(l)):
        l[i] = l[i] ** 2
    q.put(l)


def multithreading():
    q = Queue()
    threads = []
    data = [[1, 2, 3], [3, 4, 5], [4, 4, 4], [5, 5, 5]]
    for i in range(4):
        t = threading.Thread(target=job, args=(data[i], q))     # args传入的参数
        t.start()
        threads.append(t)

    for thread in threads:                                      # 添加join方法， 使得线程运行完再进行后面命令
        thread.join()
    # threads[1].join()                                         # 效果一样
    results = []
    for _ in range(4):
        results.append(q.get())
    print(results)


if __name__ == '__main__':
    multithreading()



import threading
from queue import Queue
import copy
import time


# 定义求和运算
def job(l, q):
    res = sum(l)
    q.put(res)


# 多线程运算（4线程）
def multithreading(l):
    q = Queue()
    threads = []
    for i in range(4):
        t = threading.Thread(target=job, args=(copy.copy(l), q), name='T%i' % i)
        t.start()
        threads.append(t)
    [t.join() for t in threads]
    total = 0
    for _ in range(4):
        total += q.get()
    print(total)


# 正常运算
def normal(l):
    total = sum(l)
    print(total)


if __name__ == '__main__':
    l = list(range(1000000))
    s_t = time.time()
    normal(l*4)
    print('normal: ', time.time()-s_t)
    s_t = time.time()
    multithreading(l)
    print('multithreading: ', time.time()-s_t)


import threading


# 当两个线程共享参数时，需要其中一个线程运行完毕后另一个线程在运行时，采用Lock
def job1():
    global A, lock
    lock.acquire()   # 开始运行之前上锁
    for i in range(10):
        A += 1
        print('job1', A)
    lock.release()   # 运行完毕后解锁


def job2():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 10
        print('job2', A)
    lock.release()


if __name__ == '__main__':
    lock = threading.Lock()
    A = 0
    t1 = threading.Thread(target=job1)
    t2 = threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
