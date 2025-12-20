# utils/password.py
from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希（处理bcrypt 72字节限制）"""
    # 如果密码太长，截断到72字节
    if len(password.encode('utf-8')) > 72:
        # 截断到72字节，确保不截断多字节字符
        encoded = password.encode('utf-8')[:72]
        # 尝试解码，如果失败则使用替换字符
        try:
            password = encoded.decode('utf-8')
        except UnicodeDecodeError:
            # 如果截断导致不完整的UTF-8序列，去掉最后一个字节直到可以解码
            while True:
                encoded = encoded[:-1]
                try:
                    password = encoded.decode('utf-8')
                    break
                except UnicodeDecodeError:
                    if len(encoded) == 0:
                        password = ""
                        break
    return pwd_context.hash(password)