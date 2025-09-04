# __init__方法用来为对象定制自己独有的属性
class LuffyStudent:
    school = 'luffycity' #类的数据属性
    def __init__(self,name,sex,age):
        self.Name = name
        self.Sex = sex
        self.Age = age

    def learn(self): #类的函数属性
        print('is learning')
    def eat(self):
        print('is eatting')

stu1 = LuffyStudent('王二丫','女','18')

# 加上__Init__方法后，实例化的步骤：
# 1.先产生一个空对象str1
# 2.LuffyStudent.__init??(stuq,'王二丫','女','18')

# 查
print(stu1.__dict__)
print(stu1.Name)

# 增
stu1.City = '成都'
print(stu1.City)

# 删
del stu1.City
# print(stu1.City)

# 改
stu1.Sex = '男'
print(stu1.Sex)