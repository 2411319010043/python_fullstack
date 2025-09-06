"""
在类内部定义的函数，分为两大类：
    一：绑定方法：绑定给谁，就应该由谁来调用，谁来调用就会把调用者当作第一个参数自动传入
        绑定给对象的方法：在类内定义的没有被任何装饰器修饰的
        绑定给类的方法： 在类内定义的被@classmethod装饰器修饰的方法
    二：非绑定方法：不与类或者对象绑定，不会自动传值,对象和类都可以使用 
                    用@staticmethod装饰器即可

"""


class Foo:
    def __init__(self,name):
        self.name = name 

    def tell(self):
        print('名字是%s'%self.name)

    # 绑定给类的方法
    @classmethod
    def func(cls): #cls = Foo
        print(cls)
    # 非绑定方法
    @staticmethod
    def fun1(x,y):
        print(x + y) 
    
f = Foo('egon')
#对象绑定方法
f.tell()
#类绑定方法
Foo.func() #自动传入Foo
#非绑定方法
f.fun1(1,2)
Foo.fun1(2,3)
