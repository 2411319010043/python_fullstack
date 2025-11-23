# 1. 指向 --> 将a和b都指向同一数据的地址
a = [11,22]
b = a

print(id(a))  # id可以显示变量所指向的数据的地址
print(id(b))


# 2. 深拷贝
import copy

c = copy.deepcopy(a)  # 复制数据到一个新的地址，并让c指向它
print(id(a))
print(id(c))

a.append(33)
print('a:',a)  # a: [11, 22, 33]
print('b:',b)  # b: [11, 22, 33]
print('c:',c)  # c: [11, 22]

# 3. 浅拷贝
a = [11,22]
b = [33,44]
e = [a,b]  # e -->[a的指向，b的指向]
d = copy.copy(e) # 直接复制了e的内容 
print('e:',id(e))  
print('d:',id(d))

a.append(77)
print('e:',e)  # e: [[11, 22, 77], [33, 44]]
print('d:',d)  # d: [[11, 22, 77], [33, 44]]


    # 拷贝元组
a = (11,22)
b = copy.copy(a)
c = copy.deepcopy(a)
print('a:',id(a))  # a: 2127610886336
print('b:',id(b))  # b: 2127610886336
print('c:',id(c))  # c: 2127610886336
'''
如果拷贝的是元组，那么不管是深拷贝还是浅拷贝都只会 指向
原因： 因为元组是不可变类型，那么意味着数据不可修改 因此拷贝时会自动判断 如果是元组直接指向
'''


a = [11,22]
b = [33,44]
c = (a,b)
d = copy.copy(c)  # 还是指向
e = copy.deepcopy(c) # 深拷贝
print('c:',id(c))  # c: 2033136989568
print('d:',id(d))  # d: 2033136989568
print('e:',id(e))  # e: 2033136844672
'''
若拷贝的元组含有可变类型时 浅拷贝只会指向 深拷贝会复制所有数据
'''