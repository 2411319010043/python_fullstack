import json
import os

# 生成 key
def make_cache_key(session_id, question):
    return f"{session_id}::{question.strip()}"

BASE_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(BASE_DIR,"store")
os.makedirs(CACHE_DIR,exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR,"chat_cache.json")

# 从 chat_cache.json 读取整个缓存字典；如果文件不存在，返回 {}
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data  # 返回的是字典

# 负责覆盖写入整个缓存文件，为了不丢旧数据，传给它的 cache_data 必须包含旧数据和新数据。
def save_cache(cache_data):
    with open(CACHE_FILE,"w",encoding="utf-8") as f:
        json.dump(cache_data,f,ensure_ascii=False, indent=2)

# 根据 session_id，question 生成的 key 去缓存中查找有没有对应的 value 
def get_cache(session_id, question):
    cache_data = load_cache()
    key = make_cache_key(session_id, question)
    return cache_data.get(key)

# 负责加一条缓存
def set_cache(session_id, question, data):
    key = make_cache_key(session_id, question)
    cache_data = load_cache()
    cache_data[key] = data
    save_cache(cache_data)


# 单独测试
if __name__ == "__main__":
    session_id = "u1"
    question = "什么是 LangChain?"
    data = {"answer":{"definition":"LangChain 是一个用于构建基于大语言模型（LLM）应用的开发框架。",
     "usage":"帮助开发者把模型、数据源（如数据库、文档）和工具连接起来，实现对话、问答、自动化任务等复杂功能。",
     "example":"用 LangChain 搭建一个“文档问答机器人”，让用户提问，系统从本地PDF中检索内容并生成答案。"},
     "usage":{"total_tokens":10}}
    set_cache(session_id, question, data)
    result = get_cache(session_id, question)
    print(result)
