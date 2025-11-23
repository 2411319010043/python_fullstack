class Parent(object):
    x = 1

class Child1(Parent):
    pass  # x = 2

class Child2(Parent):
    pass

print(Parent.x, Child1.x, Child2.x) # 1 1 1
Child1.x = 2
print(Parent.x, Child1.x, Child2.x) # 1 2 1
Parent.x = 3
print(Parent.x, Child1.x, Child2.x) # 3 2 3