# security.py (放在项目根目录)
import jwt
import datetime
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import tkinter as tk
from tkinter import ttk, messagebox
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import models

# JWT配置（请确保在config.py中有这些配置）
SECRET_KEY = "your-secret-key-here"  # 请改为复杂的随机字符串
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    """创建JWT访问令牌"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """获取当前用户依赖项"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 根据用户名查找用户
    user = None
    # 先查管理员（假设管理员在schools表中）
    admin_user = db.query(models.School).filter(models.School.email == username).first()
    if admin_user:
        user = admin_user
    else:
        # 查教师
        teacher_user = db.query(models.Teacher).filter(models.Teacher.email == username).first()
        if teacher_user:
            user = teacher_user
        else:
            # 查学生
            student_user = db.query(models.Student).filter(models.Student.email == username).first()
            if student_user:
                user = student_user
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user