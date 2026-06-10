from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.assistant_agent import agent
from parsers.output_parsers_demo import format_text_as_json
from tools.image_tool import image_understanding_tool


# what：定位 web 目录下的静态资源和页面文件路径
# why：后端需要拿到这些文件的绝对路径，才能正确返回前端页面和静态资源
# how：通过当前 app.py 文件的位置，拼出 static 和 templates 目录路径
WEB_DIR = Path(__file__).resolve().parent
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"


# what：创建 FastAPI 应用对象
# why：这个对象是当前 Web 项目的后端入口，所有页面和接口都挂在它上面
# how：后面通过它注册页面路由、接口路由和静态资源服务
app = FastAPI(title="LangChain Tools Agent Demo")


# what：把 static 目录暴露给浏览器访问
# why：前端页面需要加载 JavaScript 和 CSS 文件
# how：把本地 web/static 目录挂载到浏览器可访问的 /static 路径下
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# what：定义统一接口接收的请求体结构
# why：普通文本问题只需要 question，图片理解问题还需要 image_source
# how：用 Pydantic 模型描述字段，让 FastAPI 自动校验并解析 JSON
class AgentRequest(BaseModel):
    question: str
    image_source: str | None = None


# what：根据用户问题粗略判断任务类型
# why：后面的输出解析器需要知道当前回答大致属于什么类型
# how：通过简单关键词匹配，把问题分成 weather、image、search、wiki、chat
def infer_task_type(question: str) -> str:
    if "天气" in question or "温度" in question or "风速" in question:
        return "weather"
    if (
        "图片" in question
        or ".jpg" in question
        or ".png" in question
        or ".jpeg" in question
        or "image" in question
    ):
        return "image"
    if "搜索" in question or "最新" in question or "新闻" in question:
        return "search"
    if "谁是" in question or "是什么" in question or "百科" in question:
        return "wiki"
    return "chat"


# what：定义首页接口
# why：浏览器访问 / 时，需要先拿到一个 HTML 页面作为前端入口
# how：直接返回 web/templates/index.html 文件
@app.get("/")
def home() -> FileResponse:
    return FileResponse(TEMPLATES_DIR / "index.html")


# what：定义统一的 Agent 接口
# why：前端只调用这一个接口，就能测试聊天、天气、搜索、百科和图片理解
# how：如果传了 image_source 就直接走 image_understanding_tool，否则走综合 agent
@app.post("/api/agent")
def ask_agent(request: AgentRequest) -> dict:
    if request.image_source:
        final_text = image_understanding_tool.invoke(
            {
                "image_source": request.image_source,
                "question": request.question,
            }
        )
        structured = format_text_as_json("image", final_text)
        return {
            "task_type": "image",
            "answer": final_text,
            "structured": structured,
        }

    task_type = infer_task_type(request.question)
    agent_response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": request.question},
            ]
        }
    )
    final_text = agent_response["messages"][-1].content
    structured = format_text_as_json(task_type, final_text)
    return {
        "task_type": task_type,
        "answer": final_text,
        "structured": structured,
    }
