'''用户登录认证部分，需要一些基础的业务处理函数，用于支撑服务接口的功能，主要有：
根据用户名信息创建用户，验证用户密码，获取当前登录用户信息'''

from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.setting import AUTH_SCHEMA , AUTH_INIT_USER, AUTH_INIT_PASSWORD
from utils.password import get_password_hash, verify_password
from utils.token import extract_token
from .models import UserInDB
from .schemas import UserCreate
from sqlalchemy import func

# 初始化管理员账户
def init_admin_user():
    '''启动时检查数据库是否有用户，没有就创建管理员'''
    db = SessionLocal()  # 创建数据库会话
    cnt = db.query(func.count(UserInDB.username)).scalar()  # 查询数据库中的账号数量

    if cnt == 0:  # 当数据库中无账号时
        user = UserInDB(  # 创建初始账号
            username = AUTH_INIT_USER,
            hashed_password= get_password_hash(AUTH_INIT_PASSWORD)
        )
        db.add(user)
        db.commit()
    db.close()

# 查询用户
def get_user(db: Session, username: str):
    '''根据用户名从数据库查询用户'''
    return db.query(UserInDB).filter(UserInDB.username == username).first()

# 创建新用户
def create_user(db: Session, user:UserCreate):
    '''注册新用户后，立马进行哈希加密存储'''
    hashed_password = get_password_hash(user.password)  # 计算密码的哈希值
    db_user = UserInDB(username = user.username, hashed_password=hashed_password,)
    db.add(db_user)  # 将实例添加到会话
    db.commit()  # 提交
    db.refresh(db_user)  # 刷新实例
    return db_user

# 用户认证
def authenticate_user(db: Session, username: str, password: str):
    '''验证用户名和密码是否匹配，一般用来登录'''
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# 获取当前用户信息的依赖函数
async def get_current_user(
token: str = Depends(AUTH_SCHEMA),  # 依赖项，身份认证
db: Session = Depends(get_db)):  # 依赖项，数据库连接
    invalid_exception = HTTPException(  # 自定义异常
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='无效的用户任据',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:  # 捕获异常
        username: str = extract_token(token)  # 从token中解析出账号
        if username is None:  # 检测账号是否有效
            raise invalid_exception
    except JWTError:  # 出现解析异常时
        raise invalid_exception  # 抛出自定义异常
    user = get_user(db, username=username)  # 根据账号从数据库中查找用户信息
    if user is None:  # 未找到用户信息时
        raise invalid_exception  # 抛出自定义异常
    return user


