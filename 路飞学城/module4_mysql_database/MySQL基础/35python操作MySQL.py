import  pymysql
from pymysql import cursors


def create_users_table(cursor,conn):
    sql = """ create table users(
            id int primary key auto_increment,
            username varchar(50),
            password varchar(50)
    );
    """
    cursor.execute(sql)
    conn.commit()
def insert_users_record(cursor,conn):
    user = input('请输入用户名：')
    pwd = input('请输入密码:')
    sql = f"""
            insert into users(username,password)values('{user}','{pwd}')

"""
    cursor.execute(sql)
    conn.commit()
def main():

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
    create_users_table(cursor,conn)
    insert_users_record(cursor,conn)


    #4.关闭资源--游标对象、conn
    cursor.close()
    conn.close()






if __name__ =='__main__':
    main()