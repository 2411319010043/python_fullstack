"""
exec:
参数1：字符串形式的命令
参数2：全局作用域(字典形式),如果不指定默认使用globals()
参数3：局部作用域(字典形式),如果不指定默认使用locals()

"""
g = { #声明全局变量
    'x':1,
    'y':2
}

l = {} #声明局部变量

exec("""
global x,m
x = 10
m = 100

z = 3
""",g,l)

print(g)
print(l)


# python一切皆对象，对象可以怎么用？
# 1.都可以被引用   x = obj
# 2.都可以当作函数的参数传入
# 3.都可以当作返回值
# 4.都可以当作容器类的元素 l = [func,time,obj,1]

class Foo:
    pass
obj = Foo()
print(type(obj))
print(type(Foo)) #<class 'type'> 
#在 Python 中，类本身也是对象，而创建类的 "工厂" 就是 type。可以理解为：
# type 是所有类的 "元类"（metaclass）
# Foo 这个类是由 type 生成的对象，因此 type(Foo) 输出 <class 'type'>
print(type(list))


# 产生类的类称为元类，默认所有用class定义的类，他们的元类是type
# 定义类的两种方式：
#    方式一：class
class Chinese: #Chinese = type(....)
    pass
#    方式二：type
# 类的三要素：类名，类的基类们，类的名称空间
class_name = 'Chinese' #类名应该是字符串
class_Basices = (object,)
class_Body = """
country = 'China'
    
def __init__(self,name,age):
    self.name = name
    self.age = age

def talk(self,name):
    print('%s is talking' %sname)
    
"""
class_dic = {}
# 执行类体代码，将属性和方法存入class_dic
# globals() 的作用：提供执行环境 不会被存入class_dic
exec(class_Body,globals(),class_dic)
print(class_dic)
# 使用type动态创建类（参数应为class_name字符串、基类元组、类字典）
Chinese = type(class_name,class_Basices,class_dic)

print(type(Chinese))