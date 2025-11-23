import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException,status
from typing import List  # List 应该从 typing 模块导入
from sqlalchemy.orm import Session
from database import get_db
import models
import crud
import schemas  
router = APIRouter()

router = APIRouter(prefix='/courses',tags=['课程'])

@router.get("/",response_model=List[schemas.TeacherCheckCourse])
def get_courses(db:Session = Depends(get_db)):
    """获取课程列表"""
    return crud.get_all_course(db)
@router.get("{course_id}",response_model=schemas.TeacherCheckCourse)
def get_all_courses(course_id:int,db:Session = Depends(get_db)):
    """根据ID获取课程"""
    db_course = crud.get_course(db,course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404,detail='课程不存在')
    return db_course
@router.post("/",response_model=schemas.AdminCreateCourse)
def create_course(course:schemas.AdminCreateCourse,db:Session = Depends(get_db)):
    """创建"""
    return crud.create_course(db=db,course=course)
@router.delete("{course_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id:int,db:Session = Depends(get_db)):
    success = crud.delete_course(db,course_id=course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='课程不存在'
        )
    return None