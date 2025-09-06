class A:
    #属性隐藏: 在属性名前面加上__(2个)
    __x=1 #数据属性
    
    def __init__(self,name): #函数属性
        self.__name = name
    
    def __foo(self): #_A__foo
        print('run foo')

    def bar(self):
        self.__foo()
        print('from bar')
# print(A.__x) 报错
# 查看类的名称空间中有什么
# print(A.__dict__)
"""  {'__module__': '__main__', '_A__x': 1, '__init__': <function A.__init__ at 0x000001E5FE22BEB0>, '_A__foo': <function A.__foo at 0x000001E5FE22BF40>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}   """

a = A('egon')
# print(a.__dict__)  #{'_A__name': 'egon'}

a.bar()
"""
为什么通过访问不隐藏的方法 bar() 间接访问类内部的隐藏属性__foo可以访问到？
这是因为 这种变形方法是在你定义阶段就改变了的  类在定义阶段就会自动加载代码虽不会执行bar() 但是会监测内部的语法  当你在bar方法内部写入 self.__foo()的时候会自动重命名为 self._A__foo() 在你调用bar()执行的时候 也是执行的 self._A__foo() 这就导致了可以直接访问的隐藏的函数 
"""
"""
这种变形的特点：
    1.类的外部无法直接访问到
    2.类的内部可以直接访问
    3.子类无法覆盖父类__开头的属性(因为类名不同)
"""
class Foo():
    def __func(self):#_Foo__func
        print('from foo')
    
class Bar(Foo):
    def __func(self): #_Bar__func
        print('from Bar')
"""
这种变形需要注意的问题:
    1.变形只能发生在定义阶段 定义后再去增加不管用
    2.在继承中 父类若不想让子类覆盖自己的方法,可以将方法定义为私有的
"""
class B:
    __x=1

    def __init__(self,name):
        self.__name = name

print(B._B__x)
B.__y = 2
print(B.__dict__)
b = B('egon')
print(b.__dict__)
b.__age = 18 #'__age': 18
print(b.__dict__)

# 2.在继承中 父类若不想让子类覆盖自己的方法,可以将方法定义为私有的

class A:
    def __foo(self): #_A_foo
        print('A.foo')
    def bar(self):
        print('A.bar')
        self.__foo() #self._A_foo
class B(A):
    def __foo(self): #_B_foo
        print('B.foo')
b = B()
b.bar()
