# 继承：类与类之间什么是什么的关系
class ParentClass1:
    pass
class ParentClass2:
    pass
class SubClass1(ParentClass1):#继承父类
    pass
class SubClass2(ParentClass1,ParentClass2):#继承多个父类
    pass

# 查看继承的父类
print(SubClass2.__bases__)



# 属性查找
# 对象会先从自己的所在对象中查找，没有去自己所在类中查找，还没有会从父类中查找
class Foo:
    def f1(self):
        print('from Foo.f1')
    def f2(self):
        print('from Foo.f2')
        self.f1()

class Bar(Foo):
    def f1(self):
        print('from Bar.f1')

b = Bar()
b.f2()
