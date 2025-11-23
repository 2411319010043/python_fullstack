# create_root_admin.py (放在项目根目录)
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

def create_root_admin():
    """创建root管理员账户"""
    db = SessionLocal()
    try:
        # 检查是否已存在root管理员
        existing_admin = db.query(models.School).filter(models.School.email == "root@admin.com").first()
        if existing_admin:
            print("Root admin already exists")
            return
        
        # 创建root管理员
        root_admin = models.School(
            name="Root Administrator",
            email="root@admin.com",
            password="123456",
            address="System Headquarters"
        )
        
        db.add(root_admin)
        db.commit()
        print("Root admin created successfully")
        print("Email: root@admin.com")
        print("Password: 123456")
        
    except Exception as e:
        print(f"Error creating root admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    # 创建root管理员
    create_root_admin()