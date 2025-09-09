# 1.异常:异常是错误发送的信号，一旦程序出错，并且程序没有处理这个错误，就会抛出异常，并且程序运行随之终止
# 2.错误分为2种:
#   语法错误:在程序执行前就要立即改正错误

#   逻辑错误:
# ValueError
# int('aaa')

# NameError
# name

# IndexError
# l = [1,2,3]
# l[100]

# KeyError
# d = {}
# d['name']

# AttributeError
# class Foo:
#     pass

# Foo.xxx

# ZeroDivisionError
# 1/0

# TypeError:int类型不可迭代
# for i in 3:
#     pass


# 3.异常
# 强调一：错误发生的条件如果是可以预知的，此时应该用if判断去预防异常
AGE = 10
age = input('>>:').strip()

if age.isdigit():
    age = int(age)
    if age > AGE:
        print('太大了')

# 强调二：错误发生的条件如果是不可预制的，此时应该用异常处理机制 try..except
try:
    f = open("a.txt",'r',encoding='utf-8')
    print(next(f),end='')
    print(next(f),end='')
    print(next(f),end='')
    print(next(f),end='')
    print(next(f),end='')
    print(next(f),end='')
    print(next(f),end='')
    f.close()
except StopIteration:
    print('有错')

print('有错了，还能执行')