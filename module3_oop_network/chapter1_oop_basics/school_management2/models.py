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
    grade = relationship('Grade',back_populates='school')
    # 关联教师表 一对多的关系 需要些关系映射
    teachers = relationship('Teacher',back_populates='school')
# 2.教师
class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    email = Column(String(255),unique=True,index=True)
    password = Column(String(255),unique=True,index=True)

    # 关联学校表
    # 创建外键只能是id
    school_id = Column(Integer,ForeignKey('school.id'))
    # 关系映射
    school = relationship('School',back_populates='teachers')

# 3.学生表
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    email = Column(String(255),unique=True,index=True)
    password = Column(String(255),unique=True,index=True)
    school = Column(String(255),unique=True,index=True)
    card = Column(Integer,unique=True,index=True)

# 4.班级表
class Grade(Base):
    __tablename__ = "grade"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),unique=True,index=True)
    school = Column(String(255),unique=True,index=True)
    course = Column(String(255),unique=True,index=True)
    school_id = Column(Integer,ForeignKey('school.id'))
    school = relationship('School',back_populates='grade')
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

# 6.成绩表
class Grades(Base):
    id = Column(Integer,primary_key=True,index=True)
    score = Column(Integer,unique=True,index=True)
    # 关联学生表
    # 关联课程表
    # 关联班级表
    # 教师表

# 7.上课记录表
class classRecord(Base):
    id = Column(Integer,primary_key=True,index=True)
    lesson = Column(Integer,unique=True,index=True)
    date = Column(String(255),unique=True,index=True)
    # 关联课程表 班级表 学生版 教师表
