"""
配置文件
"""
"""知识储备：Pydantic库 
            1.自动验证输入数据的类型和格式是否正确
            2.自动将输入数据转为正确的
            3.环境变量管理"""
"""
配置文件使用Pydantic保证了：1.环境变量被正确读取和解析
                          2.配置值具有正确的数据类型
                          3.提供了默认值作为回退
                          4.支持从 .env 文件加载配置
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_HOST: str = "localhost" #数据库服务器地址
    MYSQL_PORT: int = 3306 #端口号
    MYSQL_USER: str = "root" #数据库用户名
    MYSQL_PASSWORD: str = "password" #数据库密码
    MYSQL_DB: str = "school_management" #数据库名
    SECRET_KEY: str = "your-secret-key" #JWT 签名密钥
    ALGORITHM: str = "HS256" #加密算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 #token有效期

    class Config:
        env_file = ".env" #创建了.env来覆盖默认值

settings = Settings()