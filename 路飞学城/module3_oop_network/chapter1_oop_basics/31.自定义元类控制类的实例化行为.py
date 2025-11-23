# 知识储备
# 内置方法(会在某种情况自动触发)：__call__方法(对象被调用会自动触发)
class Foo:
    def __call__(self, *args, **kwds):
        # print(self) #<__main__.Foo object at 0x000002C52B6DB4C0>
        # print(args) #(1, 2, 3)
        # print(kwds) #{'a': 1, 'b': 2}
        pass

obj = Foo()
obj(1,2,3,a=1,b=2) #对象被调用自动触发__call__
# 想实现 obj() 需要在类内部定义__call__方法

# 元类内部也应该有一个__call__方法,会在类实例化时(调用类)触发
# Foo(1,2,a=1) --> Foo.__call__(Foo,1,2,a=1)



# 定义元类：
class Mymeta(type):
    def __init__(self,class_name,class_bases,class_dic):

        super(Mymeta,self).__init__(class_name,class_bases,class_dic)

    def __call__(self,*args,**kwds):
        # 第一件事:造出一个空对象
        obj = object.__new__(self) 
        # 第二件事:初始化obj
        self.__init__(obj,*args,**kwds)
        # 第三件事:返回obj
        return obj



class Chinese(object,metaclass = Mymeta):
    country = 'China'

    def __init__(self,name,age):
        self.name = name
        print(type(name))
        self.age = age
        print(type(age))
    
    def talk(self):
        print('%s is talking' %self.name)
    
    

obj = Chinese('a',2) #-->  obj = Mymeta.__call__(Chinese, 'a', 2)
"""
你看似在调用类 Chinese，但 类本身其实是一个对象（它是由元类 Mymeta 造出来的）。
默认情况下，如果没改写，走的是 type.__call__；你改写了，所以执行 Mymeta.__call__。这里的 self 其实就是类对象 Chinese。

"""

print(obj.__dict__)