from fastapi.security import OAuth2PasswordBearer  # 用于 API 认证。
from urllib import parse  # 用于 URL 解析和处理。
 
# 定义配置项
JWT_SECRET_KEY = '121a7ca2894627374a4a3326bc9f7f82a10d11e9742670840e9d13928d87'
JWT_ALGORITHM = 'HS256'  # 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # WT中Token有效期
AUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl="auth/login")  # 身份认证设置
AUTH_INIT_USER = "admin"  # 管理员初始用户名，在程序首次运行时创建
AUTH_INIT_PASSWORD = "111111"  # 管理员初始密码

# 数据库配置
DB_HOST = 'localhost'  # 数据库所在的服务器地址
DB_USERNAME = 'root'  # 登录数据库的用户名
DB_PASSWORD = parse.quote('123456')  # 录数据库的密码，转义密码中的特殊字符
DB_DATABASE = 'nucleic'  # 数据库名


