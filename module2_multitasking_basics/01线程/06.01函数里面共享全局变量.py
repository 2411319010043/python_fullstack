

num = 100
nums = [11,22]

def test():
    global num
    
    num  += 100


def test2():
    nums.append(33)

    nums += [11,22]  # 报错

print(num)
print(nums)


test()
test2()


print(num)
print(nums)






'''
结论 修改全局变量不需要必须加global  主要是看到底是修改箭头的指向还是修改箭头所指向里面的内容 
    最终还要看是否数据是可变的--字符串和元组不可变

    num += 100 ---》  1.num --> 100  2. num --> 100+100=200 改变了箭头的指向
    nums.append(33)  ---》  1. num --> [11,22]  2. num --> [11,22]+[33] = [11,22,33] 修改箭头所指向里面的内容

'''