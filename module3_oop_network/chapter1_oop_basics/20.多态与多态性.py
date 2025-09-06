# 多态:同一类事物的多种形态
import abc
class Animal(metaclass=abc.ABCMeta): #同一类事物:动物
    @abc.abstractmethod #将下面这个方法标记为抽象方法 子类必须使用实现该方法 否则子类无法被实例化
    def talk(self):
        pass

class People(Animal): #动物的形态之一:人
    def talk(self):
        print('say hello')
class Pig(Animal): #动物的形态之一:猪
    def talk(cls):
        print('say aoao')
class Dog(Animal): #动物的形态之二:狗
    def talk(cls):
        print('say wang')

# 多态性:指的是可以在不考虑对象的类型的情况下直接使用对象
pig1 = Pig()
peo1 = People()
dog1 = Dog()

# 动态多态性
# pig1.talk()
# peo1.talk()
# dog1.talk()

#定义一个统一的接口
def func(animal): #animal需要接收的参数是已经被实例化的对象  否则会报错
    animal.talk()


# 鸭子类型




