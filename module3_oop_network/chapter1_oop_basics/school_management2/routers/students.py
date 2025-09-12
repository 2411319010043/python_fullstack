from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas,crud
import uvicorn

router = APIRouter(prefix='/students',tags=['学生'])

@router.get("/",response_model=List[schemas.CheckStudent])
def get_all_student(db:Session = Depends(get_db)):
    """获取学生列表"""
    return crud.get_all_student(db)
@router.get("{student_id}",response_model=schemas.CheckStudent)
def get_student(student_id:int,db:Session = Depends(get_db)):
    """根据ID获取学生"""
    get_all_student = crud.get_all_student(db,student_id=student_id)
    if get_all_student is None:
        raise HTTPException(status_code=404,detail='学生不存在')
    return get_all_student

@router.post("/",response_model=schemas.StudentCreate)
def create_student(student:schemas.StudentCreate,db:Session = Depends(get_db)):
    """创建"""
    return crud.create_student(db=db,student=student)

@router.delete("{student_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id:int,db:Session = Depends(get_db)):
    success = crud.delete_student(db,student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='学生不存在'
        )
    return None