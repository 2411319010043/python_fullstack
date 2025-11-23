# 在python2中 ---> 经典类：没有继承object的类，以及他的子类都叫经典类
class Foo:
    pass
class Bar(Foo):
    pass
# 在python2中 ---> 新式类：继承object的类，以及他的子类都叫新式类
class Foo(object):
    pass
class Bar(object):
    pass


# 在python3中 ---> 所有定义的类都默认继承了object类，都叫新式类
class Foo:
    pass
class Bar(Foo):
    pass

# 属性的查找方式：深度优先(经典类) 广度优先(新式类)
# 查看属性的查找顺序的方法： 类.mro()