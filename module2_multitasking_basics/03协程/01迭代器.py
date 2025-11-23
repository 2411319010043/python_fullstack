# 1. 如何判断一个类型是不是可以迭代的？
from collections.abc import Iterable   # 看这个类型是不是Iterable的子类
print(isinstance([11,22,33], Iterable) )  # isinstance(A,B) 检查A是不是B创出来的

# 2. 自己实现一个可以迭代的对象
class Classmate(object):
    def __init__(self):
        self.names = list()

    def add(self,name):
        self.names.append(name)
    
    def __iter__(self):
        '''如果想要一个对象称为一个 可以迭代的对象，即可以使用fro，那么必须实现__iter__方法'''
        return ClassIterator(self)
    
    
class ClassIterator(object):

    def __init__(self,obj):
        self.obj = obj

    def __iter__(self):
        pass

    def __next__(self):
        return self.obj.names[0]
    

classmate = Classmate()

classmate.add('张三')
classmate.add('李四')
classmate.add('王五')

for name in classmate:
    print(name)

'''一个对象如果有迭代器 那么一定是可迭代对象
    迭代器一定是可迭代对象
    可迭代对象不一定是迭代器'''