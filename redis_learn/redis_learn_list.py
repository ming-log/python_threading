# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/31 15:54
import redis
import time
#1.lpush(name,values)   增加（类似于list的append，只是这里是从左边新增加）--没有就新建
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

r.lpush("list1", 11, 22, 33)
print(r.lrange('list1', 0, -1))

r.rpush("list2", 11, 22, 33)  # 表示从右向左操作
print(r.llen("list2"))  # 列表长度
print(r.lrange("list2", 0, 3))  # 切片取出值，范围是索引号0-3

#2.rpush(name,values)   增加（从右边增加）--没有就新建
r.rpush("list2", 44, 55, 66)    # 在列表的右边，依次添加44,55,66
print(r.llen("list2"))  # 列表长度
print(r.lrange("list2", 0, -1)) # 切片取出值，范围是索引号0到-1(最后一个元素)

#3.lpushx(name,value)    往已经有的name的列表的左边添加元素，没有的话无法创建
r.lpushx("list10", 10)   # 这里list10不存在
print(r.llen("list10"))  # 0
print(r.lrange("list10", 0, -1))  # []
r.lpushx("list2", 77)   # 这里"list2"之前已经存在，往列表最左边添加一个元素，一次只能添加一个
print(r.llen("list2"))  # 列表长度
print(r.lrange("list2", 0, -1)) # 切片取出值，范围是索引号0到-1(最后一个元素

#4.rpushx(name,value)   往已经有的name的列表的右边添加元素，没有的话无法创建
r.rpushx("list2", 99)   # 这里"foo_list1"之前已经存在，往列表最右边添加一个元素，一次只能添加一个
print(r.llen("list2"))  # 列表长度
print(r.lrange("list2", 0, -1)) # 切片取出值，范围是索引号0到-1(最后一个元素)

#5.linsert(name, where, refvalue, value))    新增（固定索引号位置插入元素）
# 在name对应的列表的某一个值前或后插入一个新值
# 参数：
# name - redis的name
# where - BEFORE或AFTER
# refvalue - 标杆值，即：在它前后插入数据
# value - 要插入的数据
r.linsert("list2", "before", "11", "00")   # 往列表中左边第一个出现的元素"11"前插入元素"00"
print(r.lrange("list2", 0, -1))   # 切片取出值，范围是索引号0-最后一个元素

#6.r.lset(name, index, value)     修改（指定索引号进行修改）
# 对name对应的list中的某一个索引位置重新赋值
# 参数：
# name - redis的name
# index - list的索引位置
# value - 要设置的值
r.lset("list2", 0, -11)    # 把索引号是0的元素修改成-11
print(r.lrange("list2", 0, -1))

#7.r.lrem(name, value, num)    删除（指定值进行删除）
# 在name对应的list中删除指定的值
# 参数：
# name - redis的name
# value - 要删除的值
# num=0，删除列表中所有的指定值；
# num=2 - 从前到后，删除2个, num=1,从前到后，删除左边第1个
# num=-2 - 从后向前，删除2个
r.lrem("list2", "11", 1)    # 将列表中左边第一次出现的"11"删除
print(r.lrange("list2", 0, -1))
r.lrem("list2", "99", -1)    # 将列表中右边第一次出现的"99"删除
print(r.lrange("list2", 0, -1))
r.lrem("list2", "22", 0)    # 将列表中所有的"22"删除
print(r.lrange("list2", 0, -1))

#8. lpop(name)      删除并返回
r.lpop("list2")    # 删除列表最左边的元素，并且返回删除的元素
print(r.lrange("list2", 0, -1))
r.rpop("list2")    # 删除列表最右边的元素，并且返回删除的元素
print(r.lrange("list2", 0, -1))

#9. ltrim(name, start, end)     删除索引之外的值
# 在name对应的列表中移除没有在start-end索引之间的值
# 参数：
# name - redis的name
# start - 索引的起始位置
# end - 索引结束位置
r.ltrim("list2", 0, 2)    # 删除索引号是0-2之外的元素，值保留索引号是0-2的元素
print(r.lrange("list2", 0, -1))

#10. lindex(name, index)      取值（根据索引号取值）
# 在name对应的列表中根据索引获取列表元素
print(r.lindex("list2", 0))  # 取出索引号是0的值

#11. rpoplpush(src, dst)     移动 元素从一个列表移动到另外一个列表
# 从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
# 参数：
# src - 要取数据的列表的 name
# dst - 要添加数据的列表的 name
r.rpoplpush("list1", "list2")
print(r.lrange("list2", 0, -1))

#12. brpoplpush(src, dst, timeout=0)     移动 元素从一个列表移动到另外一个列表 可以设置超时
# 从一个列表的右侧移除一个元素并将其添加到另一个列表的左侧
#
# 参数：
#
# src - 取出并要移除元素的列表对应的name
# dst - 要插入元素的列表对应的name
# timeout - 当src对应的列表中没有数据时，阻塞等待其有数据的超时时间（秒），0 表示永远阻塞
r.brpoplpush("list1", "list2", timeout=2)
print(r.lrange("list2", 0, -1))

#13. blpop(keys, timeout)       一次移除多个列表
# 将多个列表排列，按照从左到右去pop对应列表的元素
# 参数：
# keys - redis的name的集合
# timeout - 超时时间，当元素所有列表的元素获取完之后，阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞
# r.brpop(keys, timeout) 同 blpop，将多个列表排列,按照从右像左去移除各个列表内的元素
r.lpush("list10", 3, 4, 5)
r.lpush("list11", 3, 4, 5)
while True:
    r.blpop(["list10", "list11"], timeout=2)
    print(r.lrange("list10", 0, -1), r.lrange("list11", 0, -1))

#14.自定义增量迭代
# 由于redis类库中没有提供对列表元素的增量迭代，如果想要循环name对应的列表的所有元素，那么就需要获取name对应的所有列表。
# 循环列表
# 但是，如果列表非常大，那么就有可能在第一步时就将程序的内容撑爆，所有有必要自定义一个增量迭代的功能：

def list_iter(name):
    """
    自定义redis列表增量迭代
    :param name: redis中的name，即：迭代name对应的列表
    :return: yield 返回 列表元素
    """
    list_count = r.llen(name)
    for index in range(list_count):
        yield r.lindex(name, index)
    return 0

# 使用
for item in list_iter('list2'): # 遍历这个列表
    print(item)





