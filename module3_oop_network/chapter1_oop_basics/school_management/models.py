from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    
    courses = relationship("Course", back_populates="school")
    instructors = relationship("Instructor", back_populates="school")
    students = relationship("Student", back_populates="school")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
    
    school = relationship("School", back_populates="courses")
    classes = relationship("Class", back_populates="course")

class Instructor(Base):
    __tablename__ = "instructors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
    
    school = relationship("School", back_populates="instructors")
    classes = relationship("Class", back_populates="instructor")

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"))
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    
    course = relationship("Course", back_populates="classes")
    instructor = relationship("Instructor", back_populates="classes")
    students = relationship("Student", back_populates="class_")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    
    school = relationship("School", back_populates="students")
    class_ = relationship("Class", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Grade(Base):
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    score = Column(Float, default=0)
    
    student = relationship("Student", back_populates="grades")
    class_ = relationship("Class")