# 在子类派生出的新的方法中重用父类的方法，1.指名道姓 不依赖于继承 2.super() 依赖继承
# class Hero:
#     def __init__(self,nickname,life_value,aggresivity):
#         self.nickname=nickname
#         self.life_value = life_value
#         self.aggresivity = aggresivity
#     def attack(self,enemy):
#         enemy.life_value -= self.aggresivity

# class Garne(Hero):
#     camp = 'demacia'

#     def attack(self,enemy):
#         # 重用方法1：指名道姓
#         Hero.attack(self,enemy)
#         print('from Garen Class')
    
# class Riven(Hero):
#     camp = 'Noxus'

# g = Garne('草丛伦',100,30)
# r = Riven('锐雯',80,50)

# print(r.life_value)
# g.attack(r)
# print(r.life_value)



# class Hero:
#     def __init__(self,nickname,life_value,aggresivity):
#         self.nickname=nickname
#         self.life_value = life_value
#         self.aggresivity = aggresivity
#     def attack(self,enemy):
#         enemy.life_value -= self.aggresivity

# class Garne(Hero):
#     def __init__(self,nickname,life_value,aggresivity,weapon):
#         Hero.__init__(self,nickname,life_value,aggresivity)
#         self.weapon = weapon
#     camp = 'demacia'

#     def attack(self,enemy):
#         # 重用方法1：指名道姓 不依赖继承
#         Hero.attack(self,enemy)
#         print('from Garen Class')
    
# class Riven(Hero):
#     camp = 'Noxus'

# g = Garne('草丛伦',100,30,'wolf')
# r = Riven('锐雯',80,50)

# print(g.__dict__)


# class Hero:
#     def __init__(self,nickname,life_value,aggresivity):
#         self.nickname=nickname
#         self.life_value = life_value
#         self.aggresivity = aggresivity
#     def attack(self,enemy):
#         enemy.life_value -= self.aggresivity

# class Garne(Hero):
#     def __init__(self,nickname,life_value,aggresivity,weapon):
#         Hero.__init__(self,nickname,life_value,aggresivity)
#         self.weapon = weapon
#     camp = 'demacia'

#     def attack(self,enemy):
#         # super(自己的类名,self).父类方法名(参数(self不用传))
#         # super(Garne,self).attack(enemy) 
#         super().attack(enemy) #简写
#         print('from Garen Class')
    
# class Riven(Hero):
#     camp = 'Noxus'

# g = Garne('草丛伦',100,30,'wolf')
# r = Riven('锐雯',80,50)

# print(r.life_value)
# g.attack(r)
# print(r.life_value)


# mro表的查找顺序:
# 首先确定一个点：产生的MRO表的顺序是根据对象所属类去生成的 
# 根据C这个类生成的查找f1() 分别是C --> A --> B --> ojbect
# 查找到A这个类的时候遇到了super方法 super()也是根据MRO表去查找的 
# 查找的顺序并不会因为在哪个类中而改变 也就是说查到A中的f1()中遇到了再次去查找f1()的代码只能接着往下找B类
class A:
    def f1(self):
        print('from A')
        super().f1()

class B:
    def f1(self):
        print('from B')

class C(A,B):   
    pass

c = C()
c.f1()
# print(C.mro())
# [<class '__main__.C'>, 
# <class '__main__.A'>, 
# <class '__main__.B'>, 
# <class 'object'>]