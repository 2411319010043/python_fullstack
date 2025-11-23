# 定义元类：
class Mymeta(type):
    def __init__(self,class_name,class_bases,class_dic):
        # 后面这个三个参数是如何传进来的？谁传的 怎么传的？
        # 是解释器本身（也就是 CPython 的 C 层逻辑）在执行 class 语句时帮你传的。
        if not class_name[0].isupper(): #isupper()结合索引可以判断单个字母是不是大写 
            # 判断首字母是不是大写也可以用 .istitle()
            raise NameError('命名错误')
        # 判断建造的类中是否有注释 没有不允许建造

        print('class_dic:',class_dic)

        # 判断是否有注释 以及注释不可以为空
        if not class_dic.get('__doc__',' ').strip():
        # if '__doc__' not in class_dic or not class_dic['__doc__'].strip():
            # 尝试获取 class_dic 中 '__doc__' 键的值（类的注释）。# 如果该键不存在（理论上不会，因为 Python 会自动添加），则返回空字符串 ''。# 最后用 strip() 移除首尾空白，判断是否为有效注释。
            raise TypeError('注释不能为空')
        
        super(Mymeta,self).__init__(class_name,class_bases,class_dic)
        #super方法可以在继承父类的基础上 加上自己新的逻辑




class Chinese(object,metaclass = Mymeta):# 请用 Mymeta 来制造 Chinese 这个类。默认情况下，Python 会用内置的 type 来创建类。
    country = 'China'
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def talk(self):
        print('%s is talking' %self.name)

# print('.......')
# class Foo:
#     pass

# print(Foo.__dict__) #字典中包含'__doc__' 用来标识类中是否有注释  '__doc__': None
"""
{'__module__': '__main__', '__dict__': <attribute '__dict__' of 'Foo' objects>, '__weakref__': <attribute '__weakref__' of 'Foo' objects>, '__doc__': None}
"""
