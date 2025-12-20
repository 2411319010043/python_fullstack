# utils/token.py
"""
最简单的 token 工具模块
包含课本需要的函数
"""

def create_token(data: dict):
    """
    创建 token（简单实现）
    
    参数：
        data: 要编码的数据，如 {'username': '张三'}
    
    返回：
        一个假的 token 字符串（实际项目需要实现 JWT）
    """
    # 最简单的实现，直接返回一个固定格式的字符串
    username = data.get('username', 'unknown')
    
    # 模拟生成一个 token
    # 实际项目应该使用 JWT 库，这里只是为了让代码能运行
    fake_token = f"fake-token-for-{username}-123456"
    
    return fake_token


def extract_token(authorization: str):
    """
    从 Authorization 头中提取 token
    
    参数：
        authorization: Authorization 头，如 "Bearer fake-token-for-张三-123456"
    
    返回：
        提取出的 token 字符串
    """
    if not authorization:
        return None
    
    # 处理 Bearer token 格式
    if authorization.startswith("Bearer "):
        return authorization[7:]  # 去掉 "Bearer " 前缀
    
    return authorization