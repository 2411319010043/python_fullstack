# 1. 如何判断一个类型是不是可以迭代的？
from collections.abc import Iterable   # 看这个类型是不是Iterable的子类
print(isinstance([11,22,33], Iterable) )  # isinstance(A,B) 检查A是不是B创出来的

# 2. 自己实现一个可以迭代的对象
class Classmate(object):
    def __init__(self):
        self.names = list()
        self.current_num = 0

    def add(self,name):
        self.names.append(name)
    
    def __iter__(self):
        '''如果想要一个对象称为一个 可以迭代的对象，即可以使用fro，那么必须实现__iter__方法'''
        return self
    
    def __next__(self):
        if self.current_num < len(self.names):
            ret = self.names[self.current_num]
            self.current_num += 1
            return ret
        else:
            raise StopIteration
    

classmate = Classmate()

classmate.add('张三')
classmate.add('李四')
classmate.add('王五')

for name in classmate:
    print(name)