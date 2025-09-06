# 抽象类：只定义规范 不实现具体的代码 为了规范子类
# 只能被继承 不能被实例化
# 1.引入abc模块
import abc
# 2.继承
class Animal(metaclass=abc.ABCMeta):
    # 3.为了保证子类必须使用这个方法名 需要在前面加一个装饰器
    @classmethod

    def walk(self):
        pass
    @classmethod

    def eat(self):
        pass

class Pig(Animal):

    def walk(cls):
        print('is walking')

    def eat(cls):
        print('is eatting')
pig = Pig()


