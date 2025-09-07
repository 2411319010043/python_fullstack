# 1.item系列:把类对象做成像字典对象一样进行操作对象属性
class Foo:
    def __init__(self,name):
        self.name = name
    def __getitem__(self, item):
        print('getitem执行了',item)
        print(type(item))
        return self.__dict__.get(item)
    
    def __setitem__(self,key,value):
        print('setitem执行了',key,value)
        self.__dict__[key] = value

    def __delitem__(self,key):
        self.__dict__.pop(key)  # del self.__dict__[key]
        print('delitem执行了',key)

obj = Foo('yy')
# 查看属性
obj['namex'] #可以像访问字典一样去访问类中的数据属性或函数属性 
print(obj['123','333'])
"""
getitem执行了 name
<class 'str'>
getitem执行了 ('123', '333')
<class 'tuple'>
"""

# 设置属性
obj['sex'] = 'male' #像字典一样去添加属性和值

obj['sex'] = 'female'
print(obj.__dict__)

#删除属性
del obj['sex'] #像字典一样删除属性
print(obj.__dict__)


# 2.__str__方法：定义后会在打印对象时触发执行,返回一个字符串形式的结果
#  python数据类型其实就是一种类
d = {'name':'egon'} #d = dict({'name':'egon'}) d其实就是字典的实例化
print('d:',d)

class People:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __str__(self):
        print('----->str')
        return '<name:%s,age:%s>' %(self.name,self.age)

obj = People('yy',22)
print(obj)  # print(obj.__str__())


# 3.__del__方法
f = open('settings.py') #打开
f.read()
f.close() #回收操作系统的资源,但变量f没有被回收
print(f) #可以打印f
f.read()#读取失败


class Open:
    def __init__(self,filename):
        print('open file....')
        self.filename = filename
    def __del__(self):#在删除对象前，自动回收操作系统的资源
        print('回收操作系统资源：self.close()')
    
f = Open('settings.py')
print('----main----------') #del f   f.__del__()