def create_num(all_num):
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        yield a  
        a, b = b, a+b
        current_num += 1

# 连续创建2个生成器对象 混合输出 查看是否会混淆输出数据
obj = create_num(10) 
obj2 = create_num(2)

ret = next(obj) # 只要是迭代器 就能用next()调用
print('obj:',ret)

ret = next(obj)
print('obj:',ret)

ret = next(obj2)
print('obj2:',ret)

ret = next(obj)
print('obj:',ret)

ret = next(obj)
print('obj:',ret)

ret = next(obj)
print('obj:',ret)

ret = next(obj2)
print('obj2:',ret)

#for num in obj:
    #print(num)
