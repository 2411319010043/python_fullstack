'''实现对person表的读写操作'''
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Person(BaseModel):
    id: Optional[int] = None  # id 可以是整数，也可以是 None（空）
    djrq: datetime
    xm: str
    xb: str
    nl: Optional[int] = None
    nldw: Optional[str] = '年'
    hjdz: Optional[str] = None
    jzdz: Optional[str] = None
    csrq: Optional[datetime] = None
    dw: Optional[str] 
    lxdh: str
    zjlb: Optional[str] = '身份证'
    zjhm: str
    tw: Optional[str]
    bz: Optional[str]

class Config:
    orm_mode = True