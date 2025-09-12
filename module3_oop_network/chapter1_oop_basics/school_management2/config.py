# 1.导入模块
from pydantic_settings import BaseSettings
# 2.定义Settings类 继承BaseSettings类
class Settings(BaseSettings):
    MYSQL_HOST:str = 'loclahost'
    MYSQL_PORT:int = 3306
    MYSQL_USER:str = 'root'
    MYSQL_PSD:int = 'root'
    MYSQL_DATABASE:str = "school_management"
    class Config:
        env_file = ".env"

settings = Settings()