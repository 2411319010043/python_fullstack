from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schemas import CheckIn
from app.database import  get_db
from .services import save_checkin, QueryParams, list_checkin
from utils.response import PageResponse

route = APIRouter(
    tags = ['登记']
)

@route.post('/submit', response_model=CheckIn)
async def submit(data: CheckIn, db: Session = Depends(get_db)):
    return save_checkin(db, data)

@ route.get('/list', response_model=PageResponse,)
async def list(params: QueryParams = Depends(), db: Session = Depends(get_db),):
    return list_checkin(db, params)
