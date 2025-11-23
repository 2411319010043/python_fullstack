"""
数据库连接
"""
# 1.导入模块
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost/school_management2"

# 创建引擎 数据库的大门或接口的管理员 他知道数据库在哪里 怎么连接 用什么密码
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建会话工厂 一个会话发放机
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

# 创建一个自己的基类继承模型类的基类
Base = declarative_base()

# 创建测试数据库能否连接成功函数
def test_connection():
    try:
        # 引擎.conncet()就是像管理员要通行证的方法 connection就是通行证
        # 
        with engine.connect() as connection:
            print('数据库连接成功')
            return True
    except Exception as e :
        print('数据库连接失败')
        return False

# 注入依赖函数
def get_db():
    db = SessionLocal #从会话发放机里哪一个具体的会话实例 给bd
    try:
        yield db
    finally:
        db.close() #用完连接自动回收

if __name__ == "__main__":
    if test_connection():
        print('连接成功')