import os  # 拼接历史文件目录

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 写聊天 prompt  给历史消息预留位置
from langchain_core.runnables.history import RunnableWithMessageHistory  # 包装 chain, 让它自动读写历史
from langchain_community.chat_message_histories.file import FileChatMessageHistory  # 把历史保存到 json 文件
from langchain_openai import ChatOpenAI  # 调用大模型

prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个友好的编程助教，请根据聊天历史回答用户问题。"),
    MessagesPlaceholder("history"),
    ("human","{question}"),
])

llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    temperature=0,
)

chain = prompt | llm

BASE_DIR = os.path.dirname(__file__)
HISTORY_DIR = os.path.join(BASE_DIR,"store")
os.makedirs(HISTORY_DIR,exist_ok=True)
def get_session_history(session_id):
    file_path = os.path.join(HISTORY_DIR,f"{session_id}.json")
    return FileChatMessageHistory(file_path)

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


if __name__ == "__main__":
    response1 = chain_with_history.invoke(
    {"question":"我叫小王，请记住。"},
    config={"configurable":{"session_id":"u1"}}
)
    print(response1.content)
    response2 = chain_with_history.invoke(
        {"question":"我叫什么？"},
        config={"configurable":{"session_id":"u2"}}
    )
    print(response2.content)

