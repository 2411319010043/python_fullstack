from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine, get_db

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management System")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# 初始化数据
def init_data(db: Session):
    # 检查是否已有数据
    if db.query(models.School).count() == 0:
        # 创建学校
        beijing_school = models.School(name="北京学校", location="北京")
        shanghai_school = models.School(name="上海学校", location="上海")
        db.add_all([beijing_school, shanghai_school])
        db.commit()
        
        # 创建课程
        linux_course = models.Course(name="Linux", duration=12, price=2000.00, school_id=beijing_school.id)
        python_course = models.Course(name="Python", duration=16, price=3000.00, school_id=beijing_school.id)
        go_course = models.Course(name="Go", duration=14, price=2500.00, school_id=shanghai_school.id)
        db.add_all([linux_course, python_course, go_course])
        db.commit()
        
        # 创建讲师
        instructor1 = models.Instructor(name="张老师", school_id=beijing_school.id)
        instructor2 = models.Instructor(name="李老师", school_id=beijing_school.id)
        instructor3 = models.Instructor(name="王老师", school_id=shanghai_school.id)
        db.add_all([instructor1, instructor2, instructor3])
        db.commit()
        
        # 创建班级
        class1 = models.Class(name="Linux班", course_id=linux_course.id, instructor_id=instructor1.id)
        class2 = models.Class(name="Python班", course_id=python_course.id, instructor_id=instructor2.id)
        class3 = models.Class(name="Go班", course_id=go_course.id, instructor_id=instructor3.id)
        db.add_all([class1, class2, class3])
        db.commit()

# 首页
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    init_data(db)
    return templates.TemplateResponse("index.html", {"request": request})

# 学生视图
@app.get("/student", response_class=HTMLResponse)
async def student_view(request: Request, db: Session = Depends(get_db)):
    schools = db.query(models.School).all()
    classes = db.query(models.Class).all()
    return templates.TemplateResponse("student.html", {
        "request": request, 
        "schools": schools,
        "classes": classes
    })

# 注册学生
@app.post("/student/register")
async def register_student(
    name: str = Form(...),
    school_id: int = Form(...),
    class_id: int = Form(...),
    db: Session = Depends(get_db)
):
    student = models.Student(name=name, school_id=school_id, class_id=class_id)
    db.add(student)
    db.commit()
    return RedirectResponse(url="/student", status_code=303)

# 讲师视图
@app.get("/instructor", response_class=HTMLResponse)
async def instructor_view(request: Request, db: Session = Depends(get_db)):
    instructors = db.query(models.Instructor).all()
    classes = db.query(models.Class).all()
    students = db.query(models.Student).all()
    return templates.TemplateResponse("instructor.html", {
        "request": request,
        "instructors": instructors,
        "classes": classes,
        "students": students
    })

# 更新成绩
@app.post("/instructor/update_grade")
async def update_grade(
    student_id: int = Form(...),
    class_id: int = Form(...),
    score: float = Form(...),
    db: Session = Depends(get_db)
):
    # 检查是否已有成绩记录
    grade = db.query(models.Grade).filter(
        models.Grade.student_id == student_id,
        models.Grade.class_id == class_id
    ).first()
    
    if grade:
        grade.score = score
    else:
        grade = models.Grade(student_id=student_id, class_id=class_id, score=score)
        db.add(grade)
    
    db.commit()
    return RedirectResponse(url="/instructor", status_code=303)

# 管理员视图
@app.get("/admin", response_class=HTMLResponse)
async def admin_view(request: Request, db: Session = Depends(get_db)):
    schools = db.query(models.School).all()
    courses = db.query(models.Course).all()
    instructors = db.query(models.Instructor).all()
    classes = db.query(models.Class).all()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "schools": schools,
        "courses": courses,
        "instructors": instructors,
        "classes": classes
    })

# 创建课程
@app.post("/admin/create_course")
async def create_course(
    name: str = Form(...),
    duration: int = Form(...),
    price: float = Form(...),
    school_id: int = Form(...),
    db: Session = Depends(get_db)
):
    course = models.Course(name=name, duration=duration, price=price, school_id=school_id)
    db.add(course)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# 创建讲师
@app.post("/admin/create_instructor")
async def create_instructor(
    name: str = Form(...),
    school_id: int = Form(...),
    db: Session = Depends(get_db)
):
    instructor = models.Instructor(name=name, school_id=school_id)
    db.add(instructor)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# 创建班级
@app.post("/admin/create_class")
async def create_class(
    name: str = Form(...),
    course_id: int = Form(...),
    instructor_id: int = Form(...),
    db: Session = Depends(get_db)
):
    class_ = models.Class(name=name, course_id=course_id, instructor_id=instructor_id)
    db.add(class_)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# API端点
@app.get("/api/schools", response_model=List[schemas.School])
async def get_schools(db: Session = Depends(get_db)):
    return db.query(models.School).all()

@app.get("/api/classes/{school_id}", response_model=List[schemas.Class])
async def get_classes_by_school(school_id: int, db: Session = Depends(get_db)):
    # 获取指定学校的班级
    classes = db.query(models.Class).join(models.Course).filter(models.Course.school_id == school_id).all()
    return classes

@app.get("/api/students/{class_id}", response_model=List[schemas.Student])
async def get_students_by_class(class_id: int, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.class_id == class_id).all()
    return students

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)