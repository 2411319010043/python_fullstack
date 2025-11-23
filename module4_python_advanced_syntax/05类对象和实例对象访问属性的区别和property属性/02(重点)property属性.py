'''
property属性 调用一个方法的时候可以让它看起来是调用了一个属性
    在实例方法前面加上@property 并且只有一个self参数
    调用时 不需括号

'''
class Goods:

    @property
    def size(self):
        return 100


obj = Goods()
ret = obj.size  # 看起来像是调用属性 其实是调用了方法
print(ret)