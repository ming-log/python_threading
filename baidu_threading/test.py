# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/7/28 11:03

from threading import Thread


class MyThread(Thread):
    def __init__(self, target_new):
        super().__init__(target=target_new)
        self.v = 11
        self.n = 10
        self.q = Queue()

    def main(self):
        print(1)

    def run(self):
        self.q.get()
        print(self.n)
        print(self.v)


def main():
    print(1)

t = MyThread(main)
t.start()
t.target_new()


class Person():
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def name1(self,name):          #定义方法名时不要和变量名一样，否则在调用的时候可能会报错。
        print('方法中名字 %s'%name)
        print('类中的名字 %s'%self.name)
    def age1(self,age):
        print('方法中的年龄 %s' %age)
        print('类中的年龄 %s' %self.age)


class New_person(Person):
    def __init__(self,new_name,new_age,sex):
        super().__init__(new_name,new_age)      # 继承父类中的变量
        self.sex=sex
    def diaoyong(self,name,age):
        self.name1(name)
        self.age1(age)
    def sex1(self,sex):
        print('方法中的性别 %s' %sex)
        print('类中的性别 %s' %self.sex)
new_p=New_person('小花','20','男')
new_p.diaoyong('小米','15')
new_p.sex1('女')
# new_p.name1('xiaohua')













from queue import Queue

q = Queue()
c = q.get()
print("getting!")
print(c)
q.put(1)










