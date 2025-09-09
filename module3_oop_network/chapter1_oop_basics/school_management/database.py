
"""
导入SQLAlchemy ORM 的核心组件,用于数据库操作以及对象关系映射
"""
# create_engine:数据库连接引擎
from sqlalchemy import create_engine, Column, Integer, String
# declarative_base:创建所有模型类的基类
from sqlalchemy.ext.declarative import declarative_base
# sessionmaker:创建数据库会话的工厂函数
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 数据库连接URL，Python应用程序能够访问和操作MySQL数据库中的school_management数据库。
# "数据库类型+Python驱动://数据库用户名:数据库密码@数据库服务器地址/要连接的数据库名称"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost/school_management"
 
""" ORM核心初始化步骤 """
# 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# 创建会话工厂
# autocommit:是否自动提交，不自动提交需要手动调用commit()
# autoflush:s是否自动刷新
# bind:绑定引擎名
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建类 declarative_base是一个函数返回一个类
Base = declarative_base()

# 测试连接的函数
def test_connection():
    try:
        #with...as...自动关闭 可以文件操作,数据库连接,网络连接
        with engine.connect() as connection: 
            print("数据库连接成功")
            return True
    # Exception:所有异常的基类,可以捕获任何异常
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

# # 定义简单的模型
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))
#     email = Column(String(100))

# def init_db():
#     # 创建所有表
#     Base.metadata.create_all(bind=engine)
#     print("✅ 数据库表创建成功！")

# 数据库会话依赖注入函数
def get_db():
    db = SessionLocal() #db = SessionLocal()
    try:
        yield db # 将会话传递给请求处理函数
    finally:
        db.close() #请求完成后关闭会话

# 测试代码
if __name__ == "__main__":
    if test_connection():
        print('连接成功')