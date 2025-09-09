# 多分支:被监测的代码块抛出的异常有多种可能性,并且我们需要针对每一种异常类型都定制专门的处理逻辑
try:
    print('---1')
    Name
    print('---2')
    l = [1,2,3]
    l[100]
    print('---3')
    d = {}
    d['name']
    print('---')
except NameError as e:
    print('---1',e)
except IndexError as e:
    print('---1',e)
except KeyError as e:
    print('---3',e)

print('继续执行')

# 万能异常 Exception

try:
    print('---1')
    Name
    print('---2')
    l = [1,2,3]
    l[100]
    print('---3')
    d = {}
    d['name']
    print('---')
except Exception as e:
    print('---1',e)

print('继续执行')

# 多分支和万能异常结合
try:
    print('---1')
    Name
    print('---2')
    l = [1,2,3]
    l[100]
    print('---3')
    d = {}
    d['name']
    print('---')
except NameError as e:
    print('---1',e)
except IndexError as e:
    print('---1',e)
except Exception as e:
    print('---3',e)

print('继续执行')



# 其他结构 else
try:
    print('---1')

    print('---2')
    l = [1,2,3]
 
    print('---3')
   
    print('---')
except NameError as e:
    print('---1',e)
except IndexError as e:
    print('---1',e)
except Exception as e:
    print('---3',e)
else:
    print('被检测的代码块没有发生异常时执行')
finally:
    print('不管被检测的代码块，有无发生异常都会执行的代码块')

# finally应用： 文件的回收
# try:
#     f = open("a.txt",'r',encoding='utf-8')
#     print(next(f),end='')
#     print(next(f),end='')
#     print(next(f),end='')
#     print(next(f),end='')
#     print(next(f),end='')
#     print(next(f),end='')
#     print(next(f),end='')
# finally:
#     f.close()

# 主动抛出异常 raise 异常类型(值)
# class People:
#     def __init__(self,name,age):
#         if isinstance(name,str) and isinstance(age,int):
#             self.name = name
#             self.age = age
#         else:
#             raise TypeError('你输入的值类型错了')
            
# p = People(11,'dd')




# 自定义异常
class MyException(BaseException):
    def __init__(self, msg):
        super(MyException,self).__init__()
        self.msg = msg
    def __str__(self):
        return "这是我自己定义的异常%s" %self

raise MyException('我自己的异常类型')
# 断言 assert

info= {}
info['name'] = 'yy'
info['age'] = 22


if 'name' not in info:
    raise KeyError
if 'age' not in info:
    raise KeyError
        # 等价于
assert 'name' in info and 'age' in info

if info['name'] == 'yy' and info['age'] == 22:
    print('welcome')