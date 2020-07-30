# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/28 9:55
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# host: host码
# port: 端口
# db: 数据库
# decode_responses: redis 取出的结果默认是字节，我们可以设定 decode_responses=True 改成字符串
r.set('foo', 'bar')
rr = r.get('foo')
print(rr)

# 连接池
# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# <==>
# r = redis.Redis(connection_pool=pool)
r.set('name', 'runoob')  # 设置 name 对应的值
print(r.get('name'))  # 取出键 name 对应的值

# redis 基本命令 String
#set(name, value, ex=None, px=None, nx=False, xx=False)
#在 Redis 中设置值，默认，不存在则创建，存在则修改。
# 参数：
# ex - 过期时间（秒）
# px - 过期时间（毫秒）
# nx - 如果设置为True，则只有name不存在时，当前set操作才执行
# xx - 如果设置为True，则只有name存在时，当前set操作才执行
#1.ex - 过期时间（秒） 这里过期时间是3秒，3秒后p，键food的值就变成None
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('food', 'mutton', ex=3)    # key是"food" value是"mutton" 将键值对存入redis缓存
print(r.get('food'))  # mutton 取出键food对应的值

#2.px - 过期时间（豪秒） 这里过期时间是3豪秒，3毫秒后，键foo的值就变成None
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('food', 'beef', px=3)
print(r.get('food'))

#3.nx - 如果设置为True，则只有name不存在时，当前set操作才执行 （新建）
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
print(r.set('fruit', 'watermelon', nx=True))    # True--不存在
print(r.get('fruit'))
# 如果键fruit不存在，那么输出是True；如果键fruit已经存在，输出是None

#4.xx - 如果设置为True，则只有name存在时，当前set操作才执行 （修改）
print((r.set('fruit', 'watermelon', xx=True)))   # True--已经存在
print(r.get('fruit'))
# 如果键fruit已经存在，那么输出是True；如果键fruit不存在，输出是None

#5.setnx(name, value)
#设置值，只有name不存在时，执行设置操作（添加）
print(r.setnx('fruit1', 'banana'))  # fruit1不存在，输出为True
print(r.get('fruit1'))

#6.setex(name, time, value)
#设置值  参数：time - 过期时间（数字秒 或 timedelta对象）
import time

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.setex("fruit2", 5, "orange")
time.sleep(5)
print(r.get('fruit2'))  # 5秒后，取值就从orange变成None

#7.psetex(name, time_ms, value)
# 设置值  参数：time_ms - 过期时间（数字毫秒 或 timedelta对象）
r.psetex("fruit3", 5000, "apple")
time.sleep(5)
print(r.get('fruit3'))  # 5000毫秒后，取值就从apple变成None

#8.mset(self, mapping)
r.mget({'k1': 'v1', 'k2': 'v2'})
r.mset({"k1":"v1", "k2":"v2"}) # 输入一个mapping对象
print(r.mget("k1", "k2"))   # 一次取出多个键对应的值
print(r.mget("k1"))

#9.mget(keys, *args)   批量获取
print(r.mget('k1', 'k2'))
print(r.mget(['k1', 'k2']))
print(r.mget("fruit", "fruit1", "fruit2", "k1", "k2"))  # 将目前redis缓存中的键对应的值批量取出来

#10.getset(name, value)   设置新值并获取原来的值
r.set("food", "beef")
old = r.getset("food", "barbecue") # 设置的新值是barbecue 设置前的值是beef
print(old)

#11.getrange(key, start, end)   获取子序列（根据字节获取，非字符）
#name - Redis 的 name
#start - 起始位置（字节）
#end - 结束位置（字节）
r.set("cn_name", "君惜大大") # 汉字
print(r.getrange("cn_name", 0, 2))   # 取索引号是0-2 前3位的字节 君 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
print(r.getrange("cn_name", 0, -1))  # 取所有的字节 君惜大大 切片操作
r.set("en_name","junxi") # 字母
print(r.getrange("en_name", 0, 2))  # 取索引号是0-2 前3位的字节 jun 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
print(r.getrange("en_name", 0, -1)) # 取所有的字节 junxi 切片操作

#12.setrange(name, offset, value)
#修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
r.setrange("en_name", 1, "ccc")
print(r.get("en_name"))    # jccci 原始值是junxi 从索引号是1开始替换成ccc 变成 jccci

#13.setbit(name, offset, value)   对 name 对应值的二进制表示的位进行操作
# name - redis的name
# offset - 位的索引（将值变换成二进制后再进行索引）
# value - 值只能是 1 或 0
# 注：如果在Redis中有一个对应： n1 = "foo"，
# 那么字符串foo的二进制表示为：01100110 01101111 01101111
# 所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，
# 那么最终二进制则变成 01100111 01101111 01101111，即："goo"
# 特别的，如果source是汉字 "陈思维"怎么办？
# 答：对于utf-8，每一个汉字占 3 个字节，那么 "陈思维" 则有 9个字节 对于汉字，for循环时候会按照 字节 迭代，
# 那么在迭代时，将每一个字节转换 十进制数，然后再将十进制数转换成二进制
# 11100110 10101101 10100110 11100110 10110010 10011011 11101001 10111101 10010000
source = "陈思维"
source = "i love you"
for i in source:
    num = ord(i)
    print (bin(num).replace('b',''))
# i love you 编码/解码
ily = ['01101001','0100000','01101100','01101111','01110110','01100101','0100000','01111001','01101111','01110101']
for i in ily:
    s = '0b' + i
    print(chr(eval(s)), end='')
print()

#14.getbit(name, offset)     获取name对应的值的二进制表示中的某位的值 （0或1）
print(r.getbit("foo1", 0)) # 0 foo1 对应的二进制 4个字节 32位 第0位是0还是1

#15.bitcount(key, start=None, end=None)   获取name对应的值的二进制表示中 1 的个数
# key - Redis的name
# start - 字节起始位置
# end - 字节结束位置
print(r.get("foo"))  # goo1 01100111
print(r.bitcount("foo",0,1))  # 11 表示前2个字节中，1出现的个数

#16.bitop(operation, dest, *keys)  获取多个值，并将值做位运算，将最后的结果保存至新的name对应的值
# operation - AND（并） 、 OR（或） 、 NOT（非） 、 XOR（异或）
# dest - 新的Redis的name
# *keys - 要查找的Redis的name
r.bitop("AND", 'new_name', 'n1', 'n2', 'n3')

r.set("foo","1")  # 0110001
r.set("foo1","2")  # 0110010
print(r.mget("foo","foo1"))  # ['goo1', 'baaanew']
print(r.bitop("AND","new","foo","foo1"))  # "new" 0 0110000
print(r.mget("foo","foo1","new"))

source = "12"
for i in source:
    num = ord(i)
    print(num)  # 打印每个字母字符或者汉字字符对应的ascii码值 f-102-0b100111-01100111
    print(bin(num))  # 打印每个10进制ascii码值转换成二进制的值 0b1100110（0b表示二进制）
    print(bin(num).replace('b',''))  # 将二进制0b1100110替换成01100110

#17.strlen(name)     返回name对应值的字节长度（一个汉字3个字节）
print(r.strlen("foo"))  # 4 'goo1'的长度是4

#18.incr(self, name, amount=1)  自增 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自增。
# name - Redis的name
# amount - 自增数（必须是整数）
r.set("foo", 123)
print(r.mget("foo", "foo1", "foo2", "k1", "k2"))
r.incr("foo", amount=1)
print(r.mget("foo", "foo1", "foo2", "k1", "k2"))
# 应用场景 – 页面点击数
# 假定我们对一系列页面需要记录点击次数。例如论坛的每个帖子都要记录点击次数，而点击次数比回帖的次数的多得多。
# 如果使用关系数据库来存储点击，可能存在大量的行级锁争用。所以，点击数的增加使用redis的INCR命令最好不过了。
# 当redis服务器启动时，可以从关系数据库读入点击数的初始值（12306这个页面被访问了34634次）
r.set("visit:12306:totals", 34634)
print(r.get("visit:12306:totals"))
#每当有一个页面点击，则使用INCR增加点击数即可。
r.incr("visit:12306:totals")
r.incr("visit:12306:totals")
print(r.get("visit:12306:totals"))
#页面载入的时候则可直接获取这个值
print(r.get("visit:12306:totals"))

#19.incrbyfloat(self, name, amount=1.0)  自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
# name - Redis的name
# amount - 自增数（浮点型）
r.set("foo1", "123.0")
r.set("foo2", "221.0")
print(r.mget("foo1", "foo2"))
r.incrbyfloat("foo1", amount=2)
r.incrbyfloat("foo2", amount=3)
print(r.mget("foo1", "foo2"))

#20.decr(self, name, amount=1)
# 自减 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自减。
# 参数：
# name - Redis的name
# amount - 自减数（整数)
r.mset({'foo4':50,'foo1':50})
r.decr("foo4", amount=3) # 递减3
r.decr("foo1", amount=1) # 递减1
print(r.mget("foo1", "foo4"))

#21.append(key, value)   在redis name对应的值后面追加内容
# 参数：
# key - redis的name
# value - 要追加的字符串
r.set('name','junxi')
r.append("name", "haha")    # 在name对应的值junxi后面追加字符串haha
print(r.mget("name"))



