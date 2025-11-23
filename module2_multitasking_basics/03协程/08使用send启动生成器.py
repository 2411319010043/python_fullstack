def create_num(all_num):
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        ret = yield a 
        print('>>>>ret>>>>',ret)
        a, b = b, a+b
        current_num += 1

obj = create_num(10)

ret = next(obj) # 一般第一次调用都用next()，用.send()可能会崩 除非使用.send(None)
print(ret)

# send里面的数据会传递给第5行，当作Yield的结果，然后ret保存这个结果
# send的结果是下一次调用yield时，yield后面的值
ret = obj.send(None) # .send()可以传参 
print(ret)







