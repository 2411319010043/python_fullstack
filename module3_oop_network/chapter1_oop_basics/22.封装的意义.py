# 1.封装数据属性:明确区别内外,
class People:
    def __init__(self,name,age):
        self.__name = name
        self.__age = age
    
    def tell_info(self):
        print('Name:<%s> Age<%s>' %(self.__name,self.__age))

    def set_info(self,name,age):
        if not isinstance(name,str):
            print('名字必须是字符串类型')
            return
        if not isinstance(age,int):
            print('年龄必须是数字类型')
            # return
        self.__name = name
        self.__age = age

p = People('egon',18)

p.set_info('nike','22')
p.tell_info()