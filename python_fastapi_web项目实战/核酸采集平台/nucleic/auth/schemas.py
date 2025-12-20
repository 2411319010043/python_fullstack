from typing import Optional
from pydantic import BaseModel  # 用于数据验证和序列化

class Token(BaseModel):  # 定义token的响应模型
    access_token: str
    token_type: str

class UserBase(BaseModel):  # 定义用户模型基类
    id: Optional[int]
    username: str

class UserCreate(UserBase):  # 用来注册用户
    password: str

class User(UserBase):  # 定义返回用户信息的响应模型 是Pydantic 和 SQLAlchemy 之间的桥梁
    '''继承了UserBase类中的字段id和username 并没有继承password'''
    class Config:
        orm_mode = True
