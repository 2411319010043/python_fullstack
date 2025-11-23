import  pymysql
from pymysql import cursors
#1.连接数据库、参数
conn = pymysql.connect(host = 'localhost',
                       port=3306,user='root',
                       password='123456',
                       database='test',
                       cursorclass= cursors.DictCursor #获取字典游标 以字典形式返回 默认是元组 
                       )

#2.获取游标对象
cursor = conn.cursor()

#3.核心--执行sql
sql = 'select * from users;'
cursor.execute(sql)
ret = cursor.fetchall() #元组类型的返回结果
print(type(ret))

for stu in ret:
    print(stu)
#4.关闭资源--游标对象、conn
cursor.close()
conn.close()












