# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/1 10:05

import redis
import time

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 1. delete(*names)  删除
# 根据删除redis中的任意数据类型（string、hash、list、set、有序set）
r.delete("gender")  # 删除key为gender的键值对

# 2. exists(name)     检查名字是否存在
# 检测redis的name是否存在，存在就是True，False 不存在
print(r.exists("zset1"))

# 3. keys(pattern='')    模糊匹配
# 根据模型获取redis的name
# 更多：
# KEYS * 匹配数据库中所有 key 。
# KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
# KEYS hllo 匹配 hllo 和 heeeeello 等。
# KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo
print(r.keys("foo*"))

# 4. expire(name ,time)   设置超时时间
# 为某个redis的某个name设置超时时间
r.lpush("list5", 11, 22)
r.expire("list5", time=3)
print(r.lrange("list5", 0, -1))
time.sleep(3)
print(r.lrange("list5", 0, -1))

# 5. rename(src, dst)   重命名
# 对redis的name重命名
r.lpush("list5", 11, 22)
r.rename("list5", "list5-1")

# 6. randomkey()    随机获取name
# 随机获取一个redis的name（不删除）
print(r.randomkey())

# 7. type(name)    获取类型
# 获取name对应值的类型
print(r.type("set1"))
print(r.type("hash2"))

# 8. 查看所有元素
r.scan(cursor=0, match=None, count=None)
print(r.hscan("hash2"))
print(r.sscan("set3"))
print(r.zscan("zset2"))
print(r.getrange("foo1", 0, -1))
print(r.lrange("list2", 0, -1))
print(r.smembers("set3"))
print(r.zrange("zset3", 0, -1))
print(r.hgetall("hash1"))

# 9. 查看所有元素--迭代器
r.scan_iter(match=None, count=None)

for i in r.hscan_iter("hash1"):
    print(i)

for i in r.sscan_iter("set3"):
    print(i)

for i in r.zscan_iter("zset3"):
    print(i)


# other 方法
print(r.get('name'))    # 查询key为name的值
r.delete("gender")  # 删除key为gender的键值对
print(r.keys())  # 查询所有的Key
print(r.dbsize())   # 当前redis包含多少条数据
r.save()    # 执行"检查点"操作，将数据写回磁盘。保存时阻塞
# r.flushdb()        # 清空r中的所有数据

# 管道（pipeline）
