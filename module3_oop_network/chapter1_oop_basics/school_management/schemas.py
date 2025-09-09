""" Pydantic模型"""
from pydantic import BaseModel
from typing import List, Optional

class SchoolBase(BaseModel):
    name: str
    location: str

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    id: int
    
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    name: str
    duration: int
    price: float
    school_id: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

class InstructorBase(BaseModel):
    name: str
    school_id: int

class InstructorCreate(InstructorBase):
    pass

class Instructor(InstructorBase):
    id: int
    
    class Config:
        from_attributes = True

class ClassBase(BaseModel):
    name: str
    course_id: int
    instructor_id: int

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    school_id: int
    class_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    student_id: int
    class_id: int
    score: float

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    
    class Config:
        from_attributes = True