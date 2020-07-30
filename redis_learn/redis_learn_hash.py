# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/7/30 14:39

# 1、hset(name, key, value)     单个增加--修改(单个取出)--没有就新增返回1，有的话不能修改返回0
# 参数：
# name - redis的name
# key - name对应的hash中的key
# value - name对应的hash中的value
import redis
import time

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

r.hset("hash1", "k1", "v1")
r.hset("hash1", "k2", "v2")
print(r.hkeys("hash1"))             # 取hash中所有的key
print(r.hget("hash1", "k1"))        # 单个取hash的key对应的值
print(r.hmget("hash1", "k1", "k2")) # 多个取hash的key对应的值
r.hsetnx("hash1", "k2", "v3")       # 只能新建
print(r.hget("hash1", "k2"))

#2、hmset(name, mapping)    批量增加（取出）
# 在name对应的hash中批量设置键值对
# 参数：
# name - redis的name
# mapping - 字典，如：{'k1':'v1', 'k2': 'v2'}
r.hmset("hash2", {"k2": "v2", "k3": "v3"})
r.hget("hash2", "k2")

# hmget(name, keys, *args)
r.hmget("hash2", "k2", "k3")

#3、 hgetall(name)     取出所有的键值对
print(r.hgetall("hash1"))

#4、 hlen(name)     得到所有键值对的格式 hash长度
print(r.hlen("hash1"))

#5、hkeys(name)     得到所有的keys（类似字典的取所有keys）
print(r.hkeys("hash1"))

#6、hvals(name)     得到所有的value（类似字典的取所有value）
print(r.hvals("hash1"))

#7、hexists(name, key)    判断成员是否存在（类似字典的in）
print(r.hexists("hash1", "k4"))  # False 不存在
print(r.hexists("hash1", "k1"))  # True 存在

#8、hdel(name,*keys)        删除键值对
print(r.hgetall("hash1"))
r.hset("hash1", "k2", "v222")   # 修改已有的key k2
r.hset("hash1", "k11", "v1")   # 新增键值对 k11
r.hdel("hash1", "k2")    # 删除一个键值对
print(r.hgetall("hash1"))

#9、hincrby(name, key, amount=1)   自增自减整数(将key对应的value--整数 自增1或者2，或者别的整数 负数就是自减)
# 自增name对应的hash中的指定key的值，不存在则创建key=amount
# 参数：
# name - redis中的name
# key - hash对应的key
# amount - 自增数（整数）
r.hset("hash1", "k3", 123)
r.hincrby("hash1", "k3", amount=-1)
print(r.hgetall("hash1"))
r.hincrby("hash1", "k4", amount=1)  # 不存在的话，value默认就是1
print(r.hgetall("hash1"))

#10、hincrbyfloat(name, key, amount=1.0)   自增自减浮点数(将key对应的value--浮点数 自增1.0或者2.0，或者别的浮点数 负数就是自减)
# 参数：
# name - redis中的name
# key - hash对应的key
# amount，自增数（浮点数）
r.hset("hash1", "k5", "1.0")
r.hincrbyfloat("hash1", "k5", amount=-1.0)    # 已经存在，递减-1.0
print(r.hgetall("hash1"))
r.hincrbyfloat("hash1", "k6", amount=-1.0)    # 不存在，value初始值是-1.0 每次递减1.0
print(r.hgetall("hash1"))

#11、hscan(name, cursor=0, match=None, count=None)   取值查看--分片读取
#增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆
# 参数：
# name - redis的name
# cursor - 游标（基于游标分批取获取数据）
# match - 匹配指定key，默认None 表示所有的key
# count - 每次分片最少获取个数，默认None表示采用Redis的默认分片个数
print(r.hscan("hash1"))

# 12、hscan_iter(name, match=None, count=None)   利用yield封装hscan创建生成器，实现分批去redis中获取数据
# 参数：
# match - 匹配指定key，默认None 表示所有的key
# count - 每次分片最少获取个数，默认None表示采用Redis的默认分片个数
for item in r.hscan_iter('hash1'):
    print(item)
print(r.hscan_iter("hash1"))    # 生成器内存地址

for i in range(1000):
    r.hset('m2','key%s'%i,'value%s'%i)
ret = r.hscan_iter('m2',count=10)
for i in ret:
    print(i)

