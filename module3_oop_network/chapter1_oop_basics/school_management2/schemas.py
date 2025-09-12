"""
围绕管理员，教师，学生的注册登录功能
"""
from typing import Optional
from pydantic import BaseModel,EmailStr

class AdminLogin(BaseModel): #定义管理员登录功能
    email:EmailStr
    password:str

class AdminCreate(AdminLogin):#定义管理员注册功能 
    username:str

class AdminResponse(BaseModel):
    name:str
    email:EmailStr

    class Config: #固定类名
        from_attributes = True #允许ORM转换

class TeacherLogin(AdminLogin):
    pass
# class TeacherCreate(AdminCreate):
#     pass 
class TeacherResponse(AdminResponse):
    id:int
    username:str
    class_id:str
    email:EmailStr
    class Config:
        from_attributes = True 

class StudentLogin(AdminLogin):
    pass 
class StudentCreate(AdminCreate):
    class_id:int
class StudentResponse(AdminResponse):
    id:int
    username:str
    class_id:str
    email:EmailStr
    class Config:
        from_attributes = True

# 管理员创建学校功能
class AdminCreateSchool(BaseModel):
    address : str
    name:str
# 管理员创建课程
class AdminCreateCourse(BaseModel):
    name : str
    cycle : int
    price : int
    outline : str
    class Config: #固定类名
        from_attributes = True #允许ORM转换
# 管理员创建班级
class AdminCreateGrade(BaseModel):
    grade : str
    course_id: int # 关联课程ID
    teacher_id: Optional[int] = None  # 关联教师ID
# 管理员创建教师
class AdminCreateTeacher(BaseModel):
    name:str
    email:EmailStr
    school_id:Optional[int] = None
    course_id:Optional[int] = None
    grade_id: Optional[int] = None   
# 管理员查看学生
class CheckStudent(BaseModel):
    name:str
    email:str
    school_id:Optional[int] = None
    course_id:Optional[int] = None
    grade_id: Optional[int] = None
    teacher_id: Optional[int] = None
    class Config: #固定类名
        from_attributes = True #允许ORM转换
# 管理员查看教师
class AdminCheckTeacher(BaseModel):
    name:str
    email:str
    school_id:Optional[int] = None
    course_id:Optional[int] = None
    grade_id: Optional[int] = None
    class Config: #固定类名
        from_attributes = True #允许ORM转换
class CheckGrade(BaseModel):
    id : int
    name : str
    course : str
    school_id :Optional[int] = None
    teacher_id :Optional[int] = None
    course:Optional[int] = None
    students :Optional[int] = None
class TeacherCreateClass_record(BaseModel):
    lesson : int
    date : str
    score : Optional[int] = None
    # 班级ID、课程ID、教师ID
    course_id:Optional[int] = None
    grade_id: Optional[int] = None
    teacher_id:Optional[int] = None

# 教师查看作业
class TeacherCheckClass_record(BaseModel):
    course_id:Optional[int] = None
    grade_id: Optional[int] = None
    homework : str
    lesson : int
    date : str
    class Config: #固定类名
        from_attributes = True #允许ORM转换

class TeacherCheckCourse(BaseModel):
    name : str
    grade_id: Optional[int] = None
    cycle : int
    price : int
    outline : str
    class Config: #固定类名
        from_attributes = True #允许ORM转换
# 学生提交作业
class StudentCommitHomework(BaseModel):
     homework:str
     class_record_id: int     # 关联上课记录ID
     student_id: int          # 学生ID
# 学生查看分数
class StudentCheckHomework(BaseModel):
    school_name:str
    course_course:str
    grade_name:str
    score: Optional[int] = None
    homework:str
    lesson:int
    class Config: #固定类名
        from_attributes = True #允许ORM转换