from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas,crud
import uvicorn

router = APIRouter(prefix='/teachers',tags=['教师'])

@router.get("/",response_model=List[schemas.AdminCheckTeacher])
def get_all_teachers(db:Session = Depends(get_db)):
    """获取教师列表"""
    return crud.get_all_teacher(db)

@router.get("{teacher_id}",response_model=schemas.AdminCheckTeacher)
def get_teacher(teacher_id:int,db:Session = Depends(get_db)):
    """根据ID获取教师"""
    db_teacher = crud.get_teacher(db,teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404,detail='教师不存在')
    return db_teacher

@router.post("/",response_model=schemas.AdminCreateTeacher)
def create_teacher(teacher:schemas.AdminCreateTeacher,db:Session = Depends(get_db)):
    """创建"""
    return crud.create_teacher(db=db,teacher=teacher)

@router.delete("{teacher_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id:int,db:Session = Depends(get_db)):
    success = crud.delete_teacher(db,teacher_id=teacher_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='教师不存在'
        )
    return None