def create_num(all_num):
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        yield a  
        a, b = b, a+b
        current_num += 1
    return 'ok。。。'


obj2 = create_num(2)

while True:
    try:
        ret = next(obj2)
        print(ret)
    except Exception as ret:
        print(ret.value) # 产生异常的时候 可以得到return的返回值
        break