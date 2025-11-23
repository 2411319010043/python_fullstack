import settings
import hashlib
import time
import random
# 1.绑定方法
class People:
    def __init__(self,name,age,sex):
        self.id = self.create_id()
        self.name = name
        self.age = age
        self.sex = sex

    def tell_info(self):
        print("name:%s,age:%s,sex:%s" %(self.name,self.age,self.sex))

    @classmethod
    def from_conf(cls):
        obj = cls(settings.name,settings.age,settings.sex)
        return obj

    @staticmethod
    def create_id():
        base_str = f"{time.time()}-{random.random()}".encode('utf-8')
        m = hashlib.md5(base_str)
        return m.hexdigest()
p = People('yy',11,'male')
#绑定给对象，就应该由该对象调用，自动将对象本身当作第一个参数传入
p.tell_info()

# 绑定给类，就应该由类调用，自动将类作为第一个参数传入
p = People.from_conf()
p.tell_info()

# 非绑定方法
p1 = People('vv',33,'female')
p2 = People('yy',11,'male')
p3 = People('ee',44,'male')

print(p1.id)
print(p2.id)
print(p3.id)