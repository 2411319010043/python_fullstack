'''使用 SQLAlchemy 创建数据库连接和 ORM 配置'''

from sqlalchemy import create_engine  # 导入创建数据库连接引擎的函数
from sqlalchemy.orm import declarative_base,sessionmaker,Session

from app.setting import *

 # 创建数据库引擎
engine = create_engine(
    f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"  # mysql://用户名:密码@主机地址/数据库名
)

# 创建会话工厂 xx = sessionmaker(是否自动提交，是否自动刷新，绑定数据库引擎)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # 创建orm基类

def get_db():
    db = SessionLocal()
    try:
        yield db  # 创建生成器函数
    finally:
        db.close()

def generate_tables():
    Base.metadata.create_all(bind=engine)