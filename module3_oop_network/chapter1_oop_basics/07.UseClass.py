class LuffyStudent:
    school = 'luffycity'
    def learn(self):
        print('is learning')
    def eat(self):
        print('is eatting')
    # 定义阶段就执行代码 分配空间
    print('我被执行了')

# 查看类的名称空间
print(LuffyStudent.__dict__)
print(LuffyStudent.__dict__['school'])