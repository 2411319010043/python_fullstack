from typing import List
from pydantic import BaseModel

class PageResponse(BaseModel):
    count: int  # 总记录数
    list: List  # 数据列表