from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# 1.学校
class School(Base):
    __tablename__ = "school"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    address = Column(String(255),unique=True,index=True)
    # 课程列表 关联课程表
    courses = relationship('Course',back_populates='school')
    # 班级列表 关联班级表
    grades = relationship('Grade',back_populates='school')
    # 关联教师表 一对多的关系 需要些关系映射
    teachers = relationship('Teacher',back_populates='school')
    # 关联学生表
    students = relationship("Student",back_populates="school")
# 2.教师
class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    email = Column(String(255),unique=True,index=True)
    password = Column(String(255),unique=True,index=True)
    # 关联上课记录表
    classRecord = relationship('Grade',back_populates='teachers')

    # 关联学校表
    # 创建外键只能是id
    school_id = Column(Integer,ForeignKey('school.id'))
    # 关系映射
    school = relationship('School',back_populates='teachers')

    #关联课程表 一个教师有一个课程表 一个课程表也只能被一名老师创建 一对一的关系

    # 关联班级表 一名教师能管一个班 一个班也只能有一个老师 一对一的关系

    # 关联学生表
    students = relationship("Student",back_populates='teacher')
    # 关联成绩表
    grades = relationship('Grades',back_populates='teachers')

# 3.学生表
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    email = Column(String(255),unique=True,index=True)
    password = Column(String(255),unique=True,index=True)
    school = Column(String(255),unique=True,index=True)
    card = Column(Integer,unique=True,index=True)
    # 关联学校表
    school_id = Column(Integer,ForeignKey("school.id"))
    school = relationship('School',back_populates="students")
    # 关联教师
    teacher_id = Column(Integer,ForeignKey("teacher.id"))
    teacher = relationship('Teacher',back_populates="students")
    # 关联上课信息表
    classRecord_id = Column(String(255))
    classRecord = relationship("classRecord",back_populates="students")
    # 关联课程表 一名学生只能查看本班一个的课程表 多对一的关系
    course_id = Column(Integer,ForeignKey('course.id'))
    course = relationship('Course',back_populates="students")
    # 关联班级表 一名学生只属于一个班级 一个班级由多名学生组成 多对一关系
    grade_id = Column(Integer,ForeignKey('Grade.id'))
    grade = relationship('Grade',back_populates="students")
    # 关联成绩表 多对多关系
    

# 4.班级表
class Grade(Base):
    __tablename__ = "grade"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    school = Column(String(255),unique=True,index=True)
    course = Column(String(255),unique=True,index=True)
    # 与学校双向关联
    school_id = Column(Integer,ForeignKey('school.id'))
    school = relationship('School',back_populates='grades')
    # 与成绩表相关联
    grades =  relationship("Grades",back_populates="grade")
    # 与教师关联 一对一关系
    # 与课程表关联 一对一关系
    # 与学生表关联
    students = relationship('Student',back_populates='grade')

# 5.课程表
class Course(Base):
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    cycle = Column(Integer,unique=True,index=True)
    price = Column(Integer,unique=True,index=True)
    outline = Column(String(255))
    # 与学校表双向关联
    school_id = Column(Integer,ForeignKey("school.id"))
    school = relationship('School',back_populates='courses')
    # 与学生关联
    students = relationship('Student',back_populates="course")
    # 与班级管理 一对一
    # 与教师关联 一对一
    # 与成绩关联 多对一
    grade_id = Column(Integer,ForeignKey('Grade.id'))
    grades = relationship('Grades',back_populates='course')
    # 与上课记录表相关联
    classRecord =  relationship("classRecord",back_populates="course")
# 6.成绩表
class Grades(Base):
    id = Column(Integer,primary_key=True,index=True)
    score = Column(Integer,unique=True,index=True)
    # 关联教师表
    teacher_id = Column(Integer,ForeignKey('teacher.id'))
    teachers =  relationship("Teacher",back_populates="grades")
    # 关联学生表 多对多

    # 关联课程表 一对多
    course = relationship('Course',back_populates="grades")
    # 关联班级表
    grade_id = Column(Integer,ForeignKey('grade.id'))
    grade =  relationship("Grade",back_populates="grades")
    # 教师表 多对一
    teachere_id = Column(Integer,ForeignKey('teacher.id'))
    teacher =  relationship("Teacher",back_populates="grades")
    # 上课记录表 一对一

# 7.上课记录表
class classRecord(Base):
    id = Column(Integer,primary_key=True,index=True)
    lesson = Column(Integer,unique=True,index=True)
    date = Column(String(255),unique=True,index=True)
    homework = Column(String(255))
    # 关联课程表 多对一
    course_id = Column(Integer,ForeignKey('course.id'))
    course =  relationship("Course",back_populates="classRecord")
    # 学生表 一对多
    #  教师表 一对多
    # 关联学生表 一张表可以被多名学生提交作业 一名学生只能提交一次
    students = relationship("Student",back_populates="classRecord")
    # 关联教师表 多对一
    teacher_id = Column(Integer,ForeignKey('teacher.id'))
    teachers =  relationship("Teacher",back_populates="classRecord")
