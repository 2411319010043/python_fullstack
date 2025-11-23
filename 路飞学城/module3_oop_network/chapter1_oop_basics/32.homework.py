"""
1.在元类中控制把自定义类的数据属性都变成大写
"""
# 元类
class Mymeta(type):
    def __new__(cls,class_name,class_bases,class_dic):
        # 定义新的字典用来存放不需要修改的和已经改为大写的
        class_dic_new = {}
        for name,value in class_dic.items(): #.items()同时获取字典中的键和值
            if (not (name.startswith('__') and name.endswith('__')) and not callable(value)): 
                class_dic_new[name.upper()] = value
            else:
                class_dic_new[name] = value
        print("修改后 class_dic_new 键:", list(class_dic_new.keys()))
        return super(Mymeta,cls).__new__(cls,class_name,class_bases,class_dic_new)
        

# 自定义类
class Foo(object,metaclass=Mymeta):
    country = 'china'
    a = 1
    def __init__(self):
        pass
    def walk(self):
        pass

print("=== 最终类字典 ===")
print(Foo.__dict__.keys())  # 查看所有键
print("\n=== 测试访问 ===")
print("Foo.COUNTRY:", Foo.COUNTRY)  # 应该输出: china
print("Foo.A:", Foo.A)              # 应该输出: 1
print("Foo.country:", hasattr(Foo, 'country'))  # 应该输出: False
print("Foo.a:", hasattr(Foo, 'a'))    


"""
在元类中控制自定义的类 无需__init__方法
    1.元类帮其完成创建对象，以及初始化操作；
    2.实例化时传参必须为关键字形式,否则抛出异常TypeError:must use keyword argument
    3.key作为用户自定义类时产生对象的属性,
"""

# 元类
class Mymeta(type):
    def __new__(cls,class_name,class_bases,class_dic):
        
        return super(Mymeta,cls).__new__(cls,class_name,class_bases,class_dic)
    def __init__(self):
        pass
    def __call__(self,*args,**kwds):
        pass
# 自定义类
class C (object, metaclass = Mymeta):
    name = 'ee'
    age = 22




