# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/1 9:53

import redis
import time

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 1.zadd(name, *args, **kwargs)  新增
r.zadd("zset1", {'n1':11, 'n2':22})
r.zadd("zset2", {'m1':22, 'm2':44})
print(r.zcard("zset1")) # 集合长度
print(r.zcard("zset2")) # 集合长度
print(r.zrange("zset1", 0, -1))   # 获取有序集合中所有元素
print(r.zrange("zset2", 0, -1, withscores=True))   # 获取有序集合中所有元素和分数


#2. zcard(name)    获取有序集合元素个数 类似于len
print(r.zcard("zset1")) # 集合长度

#3. r.zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)    获取有序集合的所有元素
# 按照索引范围获取name对应的有序集合的元素
# 参数：
# name - redis的name
# start - 有序集合索引起始位置（非分数）
# end - 有序集合索引结束位置（非分数）
# desc - 排序规则，默认按照分数从小到大排序
# withscores - 是否获取元素的分数，默认只获取元素的值
# score_cast_func - 对分数进行数据转换的函数

# 3-1 zrevrange(name, start, end, withscores=False, score_cast_func=float)    从大到小排序(同zrange，集合是从大到小排序的)
print(r.zrevrange("zset1", 0, -1))    # 只获取元素，不显示分数
print(r.zrevrange("zset1", 0, -1, withscores=True)) # 获取有序集合中所有元素和分数,分数倒序

# 3-2 zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float)    按照分数范围获取name对应的有序集合的元素
for i in range(1, 30):
   element = 'n' + str(i)
   r.zadd("zset3", element, i)
print(r.zrangebyscore("zset3", 15, 25)) # # 在分数是15-25之间，取出符合条件的元素
print(r.zrangebyscore("zset3", 12, 22, withscores=True))    # 在分数是12-22之间，取出符合条件的元素（带分数）

# 3-3 zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float)    按照分数范围获取有序集合的元素并排序（默认从大到小排序）
print(r.zrevrangebyscore("zset3", 22, 11, withscores=True)) # 在分数是22-11之间，取出符合条件的元素 按照

# 3-4 zscan(name, cursor=0, match=None, count=None, score_cast_func=float)    获取所有元素--默认按照分数顺序排序
print(r.zscan("zset3"))

# 3-5 zscan_iter(name, match=None, count=None,score_cast_func=float)    获取所有元素--迭代器
for i in r.zscan_iter("zset3"): # 遍历迭代器
    print(i)


# 4.zcount(name, min, max)   获取name对应的有序集合中分数 在 [min,max] 之间的个数
print(r.zrange("zset3", 0, -1, withscores=True))
print(r.zcount("zset3", 11, 22))

# 5.  zincrby(name, value, amount)   自增
r.zincrby("zset3", "n2", amount=2)    # 每次将n2的分数自增2
print(r.zrange("zset3", 0, -1, withscores=True))

# 6. zrank(name, value)  获取值的索引号
# 获取某个值在 name对应的有序集合中的索引（从 0 开始）
print(r.zrank("zset3", "n1"))   # n1的索引号是0 这里按照分数顺序（从小到大）
print(r.zrank("zset3", "n6"))   # n6的索引号是1

print(r.zrevrank("zset3", "n1"))    # n1的索引号是29 这里安照分数倒序（从大到小）

# 7. zrem(name, values)    删除--指定值删除
r.zrem("zset3", "n3")   # 删除有序集合中的元素n3 删除单个
print(r.zrange("zset3", 0, -1))

# 8. zremrangebyrank(name, min, max)   删除--根据排行范围删除，按照索引号来删除
r.zremrangebyrank("zset3", 0, 1)  # 删除有序集合中的索引号是0, 1的元素
print(r.zrange("zset3", 0, -1))

# 9. zremrangebyscore(name, min, max)  删除--根据分数范围删除
r.zremrangebyscore("zset3", 11, 22)   # 删除有序集合中的分数是11-22的元素
print(r.zrange("zset3", 0, -1))

# 10. zscore(name, value)  获取值对应的分数
print(r.zscore("zset3", "n27"))   # 获取元素n27对应的分数27