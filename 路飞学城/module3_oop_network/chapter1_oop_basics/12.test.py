"""
练习1：编写一个学生类，产生一堆学生对象
    有一个计数器(属性),统计总共实例了多少个对象
"""

class Stu:
    school = 'luflycity' #数据属性
    count = 0
    def __init__(self,name,sex,age):
        self.Name = name
        self.Sex = sex
        self.Age = age
        # self.count += 1
        Stu.count += 1
        
    def learn(self): #函数属性
        print('%s is learning' %self.Name)

stu1 = Stu('alex','male',18)
stu2 = Stu('fendi','female',22)
stu3 = Stu('andy','male',33)

print(stu1.count)
print(stu2.count)
print(stu3.count)


"""
练习2：模仿王者荣耀定义两个英雄类
    英雄要有昵称、攻击力、生命值等属性；
    英雄之间可以互殴，血量小于0则死亡
"""

class Hero:
    def __init__(self,name,force,life):
        self.name = name
        self.force = force
        self.life = life
    def fight(self,self2):
        while True:
            self.life -= self2.force
            self2.life -= self.force
            if self.life <=0:
                return f'{self.name}输了'
            elif self2.life <=0:
                return f'{self2.name}输了'
    

hero1 = Hero('李白',12,80)
hero2 = Hero('小乔',10,100)

# 更简洁的调用方式：通过实例调用方法
result = hero1.fight(hero2)
print(result)  # 输出战斗结果


