from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas,crud
import uvicorn

router = APIRouter(prefix='/grades',tags=['学生'])

@router.get("/",response_model=List[schemas.CheckGrade])
def get_all_grades(db:Session = Depends(get_db)):
    """获取班级列表"""
    return crud.get_all_grades(db)

@router.get("{grade_id}",response_model=schemas.CheckGrade)
def get_grade(grade_id:int,db:Session = Depends(get_db)):
    """根据ID获取班级"""
    grade = crud.get_grade(db,grade_id=grade_id)
    if grade is None:
        raise HTTPException(status_code=404,detail='班级不存在')
    return grade

@router.post("/",response_model=schemas.AdminCreateGrade)
def create_grade(grade:schemas.AdminCreateGrade,db:Session = Depends(get_db)):
    """创建"""
    return crud.create_grade(db=db,grade=grade)

@router.delete("{grade_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id:int,db:Session = Depends(get_db)):
    success = crud.delete_grade(db,grade_id=grade_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='班级不存在'
        )
    return None