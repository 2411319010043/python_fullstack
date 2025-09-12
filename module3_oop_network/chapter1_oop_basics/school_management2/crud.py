# 数据库的增删改查
# 1.导入模块
from sqlalchemy.orm import Session
import models
import schemas
# 学校数据(校区)
# 查(单条数据)
def get_school(db:Session,school_id:int):
    return db.query(models.School).filter(models.School.id == school_id).first()
# 查(全部数据)
def get_all_school(db:Session):
    return db.query(models.School).all()
# 增
def create_school(db:Session,school:schemas.AdminCreateSchool):
    db_school = models.School(**school.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school
# 删
def delete_school(db:Session,school_id:int):
    db_school = db.query(models.School).filter(models.School.id == school_id).first()
    if db_school:
        db.delete(db_school)
        db.commit()
        return True
    return False
# 改 先不改
# 教师数据
def get_teacher(db:Session,teacher_id:int):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).filter()
    return db_teacher
def get_all_teacher(db:Session):
    db_teacher = db.query(models.Teacher).all()
    return db_teacher
def create_teacher(db:Session,teacher:schemas.AdminCreateTeacher):
    db_teacher = models.Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
def delete_teacher(db:Session,teacher_id:int):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        return True
    return False

# 学生数据
# 查(单条数据)
def get_student(db:Session,student_id:int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()
#查(全部数据)
def get_all_student(db:Session):
    return db.query(models.Student).all()
# 增
def create_student(db:Session,student:schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
# 删除
def delete_student(db:Session,student_id:int):
    db_student = db.query(models.Student).filter(models.School.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False
# 课程数据()
# 查(单条数据)
def get_course(db:Session,course_id:int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    return db_course
def get_all_course(db:Session):
    return db.query(models.Course).all()
def create_course(db:Session,course:schemas.AdminCreateCourse):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
def delete_course(db:Session,course_id:int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False
# 上课记录表+成绩表
# 查(单条数据)
def get_class_record(db:Session,class_record_id:int):
    return db.query(models.class_record).filter(models.class_record.id == class_record_id).first()
def get_all_class_record(db:Session):
    return db.query(models.class_record).all()
def create_class_record(db:Session,class_record:schemas.TeacherCreateClass_record):
    db_class_record = models.Course(**class_record.model_dump())
    db.add(db_class_record)
    db.commit()
    db.refresh(db_class_record)
    return db_class_record
def delete_class_record(db:Session,class_record_id:int):
    db_class_record = db.query(models.class_record).filter(models.class_record.id == class_record_id).first()
    if db_class_record:
        db.delete(db_class_record)
        db.commit()
        return True
    return False

# 查(单条数据)
def get_grade(db:Session,grade_id:int):
    return db.query(models.Grade).filter(models.Grade.id == grade_id).first()
def get_all_grades(db:Session):
    return db.query(models.Grade).all()
def create_grade(db:Session,grade:schemas.CheckGrade):
    db_grade = models.Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade
def delete_grade(db:Session,grade_id:int):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if db_grade:
        db.delete(db_grade)
        db.commit()
        return True
    return False