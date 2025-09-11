# 数据库的增删改查
# 1.导入模块
from sqlalchemy.orm import Session
from . import models,schemas
# 学校数据(校区)
# 查
def get_school(db:Session,school_id:int):
    db_school = db.query(models.School).filter(models.School.id == school_id).first()
# 增

# 删

# 改

# 课程数据()
def get_course(db:Session,course_id:int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()