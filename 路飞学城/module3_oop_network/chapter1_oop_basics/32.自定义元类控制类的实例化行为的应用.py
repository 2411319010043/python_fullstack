# 单例模式:
# 实现方式一：
# class MySQL:
#     __instance = None #类变量，用于存储唯一的实例 防止外部直接修改
#     def __init__(self): 
#         self.host = '127.0.0.1'
#         self.port = 3306
    
#     @classmethod #绑定给类的方法
#     def singleton(cls): #传入类本身
#         if not cls.__instance:
#             obj = cls() 
#             cls.__instance = obj
#         return cls.__instance
#     def conn(self):
#         pass
#     def execute(self):
#         pass

# obj1 = MySQL.singleton()
# obj2 = MySQL.singleton()

# print(obj1)#地址一样
# print(obj2)
# print(obj1 is obj2 )

# 实现方式二：定制元类
class Mymeta(type):
      
    def __init__(self,class_name,class_bases,class_dic):
        super(Mymeta,self).__init__(class_name,class_bases,class_dic)
        self.__instance = None
    def __call__(self,*args,**kwds):

        if not self.__instance:
            obj = object.__new__(self) #造一个空对象
            
            self.__init__(self) #初始化
            self.__instance = obj #让self.__instance不再为空

        return self.__instance #返回obj
      
class MySQL(object,metaclass = Mymeta ):

    def __init__(self): 
        self.host = '127.0.0.1'
        self.port = 3306
    
    def conn(self):
        pass
    def execute(self):
        pass

obj1 = MySQL()
obj2 = MySQL()
obj3 = MySQL()
print(obj1 is obj2 is obj3)
