from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.setting import AUTH_SCHEMA
from utils.token import create_token
from .schemas import Token, User, UserCreate
from .services import authenticate_user, get_user, create_user, get_current_user

# 创建路由
route = APIRouter(
    tags=['登录']
)

# 登录接口
@route.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 验证用户凭据
    user = authenticate_user(db, form.username, form.password)
    # 如果验证失败 返回401
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码无效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 验证成功，生成JWT token
    access_token = create_token(data={'username':user.username})
    # 返回token
    return {"access_token": access_token, "token_type": "bearer"}

# 创建用户接口
@route.post("/createuser",
            dependencies=[Depends(AUTH_SCHEMA)])
async def createuser(user: UserCreate, db: Session = Depends(get_db)):
    dbuser = get_user(db, user.username)
    if dbuser:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户已存在",
        )
    return create_user(db, user)

# 获取用户信息接口
@route.get("/userinfo", response_model=User)  
async def userinfo(user: User= Depends(get_current_user)):
    return user



