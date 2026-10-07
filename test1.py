"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : main.py
@File : test1.py
@Author : 帅张张
@Time : 2025/12/29 22:49

"""


class A:
    def method(self):
        print("A's method")


class B(A):
    def method(self):
        print("B's method")
        super().method()


class C(A):
    def method(self):
        print("C's method")
        super().method()


class D(B, C):
    def method(self):
        print("D's method")
        super().method()


class E(D):
    def method(self):
        print("E's method")
        super().method()


# 创建 D 类的实例
e = E()
e.method()

# 查看 D 类的 MRO
print(E.__mro__)

class A(object):
    def __exit__(self):
        pass