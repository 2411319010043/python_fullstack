# 生成器是一种特殊的迭代器
    # 普通的迭代器必须有__iter__(),__next__()方法 生成器只需要函数内有yield
#一、普通方法实现斐波那契数列
def create_num(all_num):
    a = 0
    b = 1
    current_num = 0
    while current_num < all_num:
        print(a)
        a, b = b, a+b
        current_num += 1

create_num(10)


#二、使用生成器实现斐波那契数列
def create_num(all_num):
    print('------1------')
    #a = 0
    #b = 1
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        print('------2------')
        #print(a)
        yield a  # 如果一个函数中有yield语句，那么这个就不再是函数，而是一个生成器的模板
        print('------3------')
        a, b = b, a+b
        current_num += 1
        print('------4------')

# 如果在调用create_num的时候，发现这个函数中有yield那么此时，不是调用函数，而是创建一个生成器对象
obj = create_num(10) # obj是生成器对象

print('------5------')
ret = next(obj) # yield会把值给next()
print('------6------')
print(ret)

print('------7------')
ret = next(obj)
print('------8------')
print(ret)
print('------9------')

#for num in obj:
    #print(num)

