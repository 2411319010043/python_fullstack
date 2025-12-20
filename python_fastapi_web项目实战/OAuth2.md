# OAuth2

## what

OAuth2PasswordBearer 是FastAPI内置的类，专门用于token令牌的认证

## how

* 导入模块
* 创建OAuth2方案

```python
from fastapi.security import OAuth2PasswordBearer
from urllib import parse

AUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl= '登录路径')
```

## why

1. **标准化**：统一Token提取方式，避免每个开发者重复实现
2. **安全合规**：强制使用Bearer Token标准（RFC 6750）
3. **开发者体验**：
   - 自动生成OpenAPI/Swagger文档
   - 统一的错误响应格式
   - 清晰的依赖声明

# Parse

## what

python标准库中的 **URL编码/解码模块**

## how

```python
from urllib import parse
encoded = quote(password)
```

## why

*  URL语法冲突

  - ```python
    URL_语法 = "协议://用户:密码@主机/路径?参数#片段"
    冲突 = {
        ":": "分隔用户名密码，但密码可能包含:",
        "@": "分隔凭据和主机，但密码可能包含@", 
        "/": "分隔路径，但数据库名可能包含/",
        "?": "开始查询，但密码可能包含?",
        "#": "开始片段，但密码可能包含#"
    }
    ```

​	