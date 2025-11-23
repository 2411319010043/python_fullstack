# 一、 range
x = range(10) # 只创建range对象 占用内存小

# 二、 迭代器和range的关系
# range不是迭代器而是可迭代对象
'''
特性	    range对象	    从range获得的迭代器
可迭代	        是	                是
是迭代器	   不是	                是
可重复使用	    可以	           只能一次
内存占用	    很小	            很小
支持 next()	    不支持	            支持
'''

# 三、 实现斐波那契数列
    # 1. 传统方法
nums = list()

a = 0
b = 1
i = 0
while i < 10:
    nums.append(a)
    a, b = b, a+b
    i += 1

for num in nums:
    print(num)

    # 2. 利用迭代器
class Fibonacci(object):
    def __init__(self, all_num):
        self.all_num = all_num
        self.current_num = 0
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.current_num < self.all_num:
            ret = self.a
            self.a, self.b = self.b, self.a+self.b
            self.current_num += 1
            return ret
        else:
            raise StopIteration
        

fibo = Fibonacci(10)


for num in fibo:
    print(num)