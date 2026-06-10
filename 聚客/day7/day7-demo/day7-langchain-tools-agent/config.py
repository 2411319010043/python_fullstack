import os 
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# what：定位当前项目根目录
# why：config.py 就在项目根目录下，可以用它稳定找到 .env
# how：Path(__file__).resolve().parent 获取 config.py 所在文件夹
PROJECT_ROOT = Path(__file__).resolve().parent
# what：定位项目根目录下的 .env 文件
# why：避免因为运行目录不同导致 load_dotenv 找不到配置
# how：PROJECT_ROOT / ".env" 拼出 .env 的完整路径
ENV_PATH = PROJECT_ROOT / ".env"
# what：加载 .env 文件中的环境变量
# why：让 os.getenv 可以读取 API key、base_url、天气 API 地址等配置
# how：dotenv_path 指定 .env 路径，override=True 允许 .env 覆盖已有环境变量
load_dotenv(dotenv_path=ENV_PATH, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

GEO_URL = os.getenv("GEO_URL")
WEATHER_URL = os.getenv("WEATHER_URL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# what：创建项目统一使用的聊天模型
# why：避免每个文件重复写 ChatOpenAI(...) 配置
# how：从 config.py 中读取模型名、API_KEY、BASE_URL、temperature 固定为 0
def create_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        temperature=0
    )

