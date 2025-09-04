class LuffyStudent:
    school = 'luffycity' #类的数据属性
    def __init__(self,name,sex,age):
        self.Name = name
        self.Sex = sex
        self.Age = age

    def learn(self): #类的函数属性
        print('%s is learning' %self.Name)
        print('我是self:',self)
    def eat(self):
        print('%s is eatting' %self.Name)

stu1 = LuffyStudent('王二丫','女','18')
stu2 = LuffyStudent('张铁蛋','男','38')
stu2 = LuffyStudent('李三炮','男','48')
# 对象：特征与技能的结合体
# 类：是一系列对象相似特征与相似技能的结合体

# 类中的数据属性
# 类中的数据属性是所有对象共有的
print(f'{stu1.Name}的学校:{stu1.school}，学校的id:{id(stu1.school)}')
print(f'{stu2.Name}的学校:{stu2.school}，学校的id:{id(stu2.school)}')
print(f'{stu1.Name}的名字:{stu1.Name}，名字的id:{id(stu1.Name)}')
print(f'{stu2.Name}的名字:{stu2.Name}，名字的id:{id(stu2.Name)}')

# 类中的函数属性：是绑定给对象使用的，绑定到不同的对象是不同的绑定方法
            #    对象调用绑定方法时，会把对象本身当作第一个参数传入
print(LuffyStudent.learn) #普通函数
LuffyStudent.learn(stu1)
print('----------------------------------------------------------')
print(stu1.learn)#绑定函数
stu1.learn() #learn(stu1)
print(stu2.learn)

# 对象和类中的属性冲突,优先使用对象中的,没有了才取类中找
stu1.x = 'from stu1'
LuffyStudent.x = 'from LuffyStudent'
print(stu1.x)

