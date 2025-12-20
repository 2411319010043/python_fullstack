from typing import Optional
from sqlalchemy.orm import Session
from .schemas import CheckIn
from .models import CheckInDB
from sqlalchemy import func
from person.models import PersonInDB

class QueryParams:
    def __init__(self,
                 xm: Optional[str] = None,
                 lxdh: Optional[str] = None,
                 jzdz: Optional[str] = None,
                 bqbh: Optional[str] = None,
                 cjry: Optional[int] = None,
                 zjhm: Optional[str] = None,
                 page: Optional[int] = 1,
                 size: Optional[int] = 10):
        self.xm = xm
        self.lxdh = lxdh
        self.jzdz = jzdz
        self.bqbh = bqbh
        self.cjry = cjry
        self.zjhm = zjhm
        self.page = page
        self.size = size

def save_checkin(db: Session, data: CheckIn):
    dbdata = CheckInDB(person_id=data.person_id, bqbh=data.bqbh, bqxh = data.bqxh, 
                       cjdd=data.cjdd, cjry=data.cjry)
    db.add(dbdata)
    db.commit()
    db.refresh(dbdata)
    return dbdata

def list_checkin(db: Session, params: QueryParams):
    qcnt = db.query(func.count(CheckInDB.id))
    q = db.query(
        CheckInDB.id.label('id'),
        CheckInDB.bqbh.label('bqbh'),
        CheckInDB.bqxh.label('bqxh'),
        CheckInDB.cjdd.label('cjdd'),
        CheckInDB.cjry.label('cjry'),
        PersonInDB.djrq.label('djrq'),
        PersonInDB.id.label('person_id'),
        PersonInDB.xm.label('xm'),
        PersonInDB.xb.label('xb'),
        PersonInDB.nl.label('nl'),
        PersonInDB.nldw.label('nldw'),
        PersonInDB.hjdz.label('hjdz'),
        PersonInDB.jzdz.label('jzdz'),
        PersonInDB.csrq.label('csrq'),
        PersonInDB.dw.label('dw'),
        PersonInDB.lxdh.label('lxdh'),
        PersonInDB.zjlb.label('zjlb'),
        PersonInDB.zjhm.label('zjhm'),
        PersonInDB.tw.label('tw'),
        PersonInDB.bz.label('bz')
    ).outerjoin(PersonInDB)
    conditions = []
    if params.xm:
        conditions.append(PersonInDB.xm == params.xm)
    if params.lxdh:
        conditions.append(PersonInDB.lxdh == params.lxdh)
    if params.jzdz:
        conditions.append(PersonInDB.jzdz == params.jzdz)
    if params.zjhm:
        conditions.append(PersonInDB.zjhm == params.zjhm)
    if params.bqbh:
        conditions.append(CheckInDB.bqbh == params.bqbh)
    if params.cjry:
        conditions.append(CheckInDB.cjry == params.cjry)
    cnt = qcnt.filter(*conditions).scalar()
    data = q.filter(*conditions).limit(params.size).offset((params.page - 1) * params.size)
    return {'count': cnt, 'list': data.all()}
