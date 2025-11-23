# 计算一个人的BMI值 体重(kg)/(身高(m) ** 2)
class People:
    def __init__(self,name,weight,height):
        self.name = name
        self.weight = weight
        self.height = height
    @property #bmi本质是一个名词 和名字,身高,体重是一样的，但需要通过计算才能得到
    #           为了优化使用者体验，利用property装饰器可以将一个函数伪装成数据属性调用
    def bmi(self):
        return self.weight / (self.height ** 2)
    
p = People('yy',56,1.69)
print(p.bmi)
# p.bmi = 123   #报错 被装饰后的数据属性也不能被赋值 本质还是一个方法

# 扩展
class P:
    def __init__(self,name):
        self.__name = name
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,val):
        if not isinstance(val,str):
            print('名字必须是字符串类型')
            return
        self.__name = val
    @name.deleter
    def name(self):
        print('deleter')
        print('不允许删除')

p = P('egon')

p.name = '111'
print(p.name)

del p.name