# main.py
from fastapi import FastAPI
from database import engine, Base
from models import School,Teacher,Table,Student,Grade,class_record,Course,student_class_record_association
from routers import courses,grade,students,teachers # 导入你的其他路由
from crud import create_class_record,create_course,create_grade,create_school,create_student,create_teacher,get_class_record,get_all_class_record,get_all_course,get_all_grades,get_all_school,get_all_student,get_all_teacher,get_course,get_grade,get_school,get_student,get_teacher,delete_grade,delete_class_record,delete_course,delete_school,delete_student,delete_teacher
# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management System")

# 包含路由
app.include_router(courses.router)
app.include_router(grade.router)
app.include_router(students.router)
app.include_router(teachers.router)
# app.include_router(courses.router)  # 包含其他路由

@app.get("/")
def read_root():
    return {"message": "School Management System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
# 创建表
Base.metadata.create_all(bind=engine)
print("数据库表创建成功！")  # 添加这行来确认执行