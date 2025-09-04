class LuffyStudent:
    school = 'luffycity' #类的数据属性
    def learn(self): #类的函数属性
        print('is learning')
    def eat(self):
        print('is eatting')
    # 定义阶段就执行代码 分配空间
    print('我被执行了')

# 查看类的名称空间
print(LuffyStudent.__dict__)
print(LuffyStudent.__dict__['school'])
print(LuffyStudent.__dict__['learn'])

# 查
print(LuffyStudent.school)
print(LuffyStudent.learn)

# 增
LuffyStudent.country = 'china'
print(LuffyStudent.country)

# 删
del LuffyStudent.country
# print(LuffyStudent.country)

# 改
LuffyStudent.school = 'heima'
print(LuffyStudent.school)

stu1 = LuffyStudent()
stu2 = LuffyStudent()
stu3 = LuffyStudent()

# 类的两大作用：1.对属性操作 2.实例化出对象