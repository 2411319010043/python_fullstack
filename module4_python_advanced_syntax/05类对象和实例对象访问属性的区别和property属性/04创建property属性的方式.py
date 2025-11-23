'''
经典类 
    定义特征：Python2中不继承object的类
    限制条件：仅支持@property一种装饰器方式
    版本差异：Python3默认继承object，不写也是新式类
    
新式类 
    定义特征：继承object的类（Python3默认）
    扩展功能：支持三种装饰器方式：
        @property - 属性获取
        @方法名.setter - 属性设置
        @方法名.deleter - 属性删除
    方法要求：setter方法必须多一个value参数，deleter方法无额外参数
'''