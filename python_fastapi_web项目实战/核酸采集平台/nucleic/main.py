import uvicorn
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware  # 导入ASGI类中间件
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.database import generate_tables
from app.setting import AUTH_SCHEMA
from auth.router import route as auth_router
from auth.services import init_admin_user
from checkin.router import route as checkin_router
from person.router import route as person_router

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(  # .add_middleware是fastapi中的一个方法 用来对中间件初始化
    CORSMiddleware,  # 将导入的类配置到初始化中
    allow_origins=origins,  # 允许访问的地址
    allow_credentials=True,  # 允许带登录信息
    allow_methods=["*"],  # 所有的请求方法都允许
    allow_headers=["*"],  # 不限制请求头
)

 ## 注册应用路由，每个路由对应一个模块 ##
app.include_router(checkin_router,  # #注册登记模块
                   prefix='/checkin',  # 设置 URL 前缀
                   dependencies=[Depends(AUTH_SCHEMA)])  # 该路由下的所有端点都需要先通过 AUTH_SCHEMA 的认证。
app.include_router(person_router,prefix='/person')  # 注册预约模块
app.include_router(auth_router,prefix='/auth')  # 注册安全模块

# 挂载
#app.mount('/web', StaticFiles(directory='web/dist'), 'web') 
#app.mount('/h5', StaticFiles(directory='h5/dist'), 'h5') 

 ## 定义根路由路径指向的页面 ##
#@app.get('/')
#def toweb():
    #return RedirectResponse('/web/index.html')  # RedirectResponse就是告诉浏览器"请跳转到另一个网址"
@app.get("/")
async def root():
    return {
        "message": "核酸采集平台API服务",
        "docs": "/docs",
        "redoc": "/redoc"
    }
## 生成表结构，SQLAlchemy的数据表同步工具 ##
generate_tables()

##创建初始管理员账号##
init_admin_user()

if __name__ == '__main__':
    uvicorn.run(app=app)
