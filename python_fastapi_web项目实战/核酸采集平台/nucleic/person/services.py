'''用 SQLAlchemy 操作数据库，实现预约人员信息的：新增、查询单个、条件分页查询
    前端 → router接口（API）→ services(增删改查) → models.py(用orm写出来的数据库表) → 数据库'''

from typing import Optional

from sqlalchemy.orm import Session  # Session是数据库操作的临时窗口，想要增删改查数据库里的东西必须有Session
from sqlalchemy import func  # func是用来调用 数据库里的函数

from .schemas import Person  # Pydantic模型，用来接收前端传来的数据 + 校验格式
from .models import PersonInDB  # 导入数据库表

'''把前端传来的查询参数，统一整理成一个字典'''
async def get_params(xm: Optional[str] = None,
                     lxdh: Optional[str] = None,
                     jzdz: Optional[str] = None,
                     page: Optional[int] = 1,
                     size: Optional[int] = 10):
    return {'xm': xm, 'lxdh': lxdh, 'jzdz': jzdz, 'page': page, 'size': size}

'''保存人员信息（新增）'''
def save_person(db: Session, data: Person):  
    # db:数据库会话(并非数据库本身，你每一次对数据库的增删改查，都必须发生在一个 Session 里。)  data:前端传来的人员信息
    dbdata = PersonInDB(**data.model_dump())  # data.model_dump():把Pydantic对象转成字典 PersonInDB(**dict)创建一个数据库对象(还没进数据库)
    db.add(dbdata)  # 告诉数据库，准备插入一条新数据
    db.commit()  # 提交事务
    db.refresh(dbdata)  # 刷新
    return dbdata  # 给router接口返回数据

'''根据证件号码查一个人'''
def get_person(db: Session, zjhm):
    data = db.query(PersonInDB).filter(PersonInDB.zjhm == zjhm).first()
    return data

'''条件 + 分页查询（重点）'''
def list_person(db: Session, params):
    qcnt = db.query(func.count(PersonInDB.id))  # 存储符合条件的总记录数
    q = db.query(PersonInDB)  # 查询数据本身
    if params['xm']:  # 如果传入姓名，就加where条件查询
        q = q.filter(PersonInDB.xm == params['xm'])
        qcnt = qcnt.filter(PersonInDB.xm == params['xm'])
    if params['lxdh']:
        q = q.filter(PersonInDB.lxdh == params['lxdh'])
        qcnt = qcnt.filter(PersonInDB.lxdh == params['lxdh'])
    if params['jzdz']:
        q = q.filter(PersonInDB.jzdz.like('%' + params['jzdz'] + '%'))
        qcnt = qcnt.filter(PersonInDB.jzdz.like('%' + params['jzdz'] + '%'))
    cnt = qcnt.scalar()  # 
    data = q.limit(params['size']).offset((params['page'] - 1) * params['size'])
    return {'count': cnt, 'list': data.all()}
