# 反射:通过字符串映射到对象的属性
class People:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def talk(self):
        print('%s is talking' %self.name)

obj = People('egon',18)

print(obj.name) #obj.__dict__['name']
print(obj.talk)

# choice = input('>>:') #choice = 'name'
# print(obj.choice) #print(obj.'name')

# 判断对象 obj 是否具有名为 name 的属性
print(hasattr(obj,'name')) # obj.name --> obj.__dict__['name']
print(hasattr(obj,'talk')) #obj.talk

# 获取对象 obj 中名为 name 的属性值
print(getattr(obj,'namexxx',None))
getattr(obj,'talk',None)() #执行talk()

# 增加属性
setattr(obj,'sex','male') #obj.sex = 'male'
print(obj.sex)

# 删除
delattr(obj,'age') #del obj.age
print(obj.__dict__)


# 反射的应用一 方法的选择：
# class Service:
#     def run(self):
#         while True:
#             cmd = input('>>:').strip() #.strip()可以移除用户输入前后的空白字符
#             if hasattr(self,cmd):
#                 getattr(self,cmd)()
#     def get(self):
#         print('get......')
#     def put(self):
#         print('put........')

# obj = Service()
# obj.run()

# 反射的应用二 文件操作：

class F:
    def run(self):
        while True:
            inp = input('>>:').strip() #.strip()可以移除用户输入前后的空白字符
            # inp = 'get a.txt'
            if inp == ',':
                break
            cmds = inp.split() #对'get a.txt'进行分割 cmds = ['get','a.txt']
            # print('cmds:',cmds)
            if hasattr(self,cmds[0]):
                func = getattr(self,cmds[0])
                func(cmds)
            
    def get(self,cmds):
        print('get......%s' %cmds)
    def put(self,cmds):
        print('put........',cmds)

file = F()
file.run()