class People:
    school = 'luflycity'
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex

class Teacher(People):
    def __init__(self,name,age,sex,level,salary):
        super().__init__(name,age,sex)
        # 已经继承了父类为什么还需要调用super?
        # 继承让子类 “拥有” 父类的方法和属性，但子类的 __init__ 方法会覆盖父类的 __init__ 方法（如果子类定义了自己的 __init__）。因此还需要显式调用。通过 super().__init__() 显式调用父类的构造方法，才能让父类的属性也得到初始化：
        self.level = level
        self.salary = salary
    def teach(self):
        print('%s is teaching' %self.name)

class Student(People):
    def __init__(self,name,age,sex,class_time):
        super().__init__(name,age,sex)
        self.class_time = class_time
    def learn(self):
        print('%s is learning' %self.name)

class Course:
    def __init__(self,course_name,course_price,course_period):
        self.course_name = course_name
        self.course_price = course_price
        self.course_period = course_period
    def tell_info(self):
        print('课程名<%s> 课程价钱<%s> 课程周期<%s>' %(self.course_name,self.course_price,self.course_period))
    
class Date:
    def __init__(self,year,mon,day):
        self.year = year
        self.mon  = mon
        self.day = day
    def tell_date(self):
        print('年<%s> 月<%s> 日<%s>' %(self.year,self.mon,self.day))


# 实例化
teacher1 = Teacher('alex',18,'male',10,5000)
student1 = Student('mike',28,'female','08:30:00')
python = Course('python',3000,'3mons')
linux = Course('linux',2000,'4mons')
#老师，学生与课程是包含的关系 只需要添加课程属性，不能继承 继承是什么是什么的关系
teacher1.course = python
student1.course1 = python
student1.course2 = linux
student1.date = Date('2001','12','22')

print(teacher1.course.course_name) #老师1教授课程名
teacher1.course.tell_info()#老师1教授课程信息

# student1.course1.tell_info()
# student1.course2.tell_info()
student1.courses = []
student1.courses.append(python)
student1.courses.append(linux)
student1.date.tell_date()
"""
student1.courses = [
    <Course object at 0x00000123>,  # 第一个元素：python课程对象（包含name=python, price=3000等属性）
    <Course object at 0x00000456>   # 第二个元素：linux课程对象（包含name=linux, price=2000等属性）
]
"""
# 遍历输出
for course in student1.courses:
    print(f'课程名称:{course.course_name},课程价钱:{course.course_price},课程周期:{course.course_period}')


