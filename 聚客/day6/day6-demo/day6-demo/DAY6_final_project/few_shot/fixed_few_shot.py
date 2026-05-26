import os

from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

examples = [
    {"question":"什么是LangChain?",
     "definition":"LangChain 是一个用于构建基于大语言模型（LLM）应用的开发框架。",
     "usage":"帮助开发者把模型、数据源（如数据库、文档）和工具连接起来，实现对话、问答、自动化任务等复杂功能。",
     "example":"用 LangChain 搭建一个“文档问答机器人”，让用户提问，系统从本地PDF中检索内容并生成答案。"},

    {"question":"什么是PromptTemplate?",
     "definition":"PromptTemplate 是一种“提示词模板”，用于动态生成发送给AI的 Prompt。",
     "usage":"把固定内容和变量组合起来，避免手动拼接字符串，让 Prompt 更规范、可复用。",
     "example":"使用 PromptTemplate 可以把“请把{word}翻译成英文”中的 {word} 动态替换成“苹果”，最终生成“请把苹果翻译成英文”。"},
    
    {"question":"什么是Runnable?",
     "definition":"Runnable 是 LangChain 中统一的执行接口，用来定义模型、Prompt 和工具的调用流程。",
     "usage":"可以把多个组件串联起来，形成完整的 AI 处理链，支持同步、异步和流式输出。",
     "example":"使用 Runnable 可以把“Prompt模板 + 大模型 + 输出解析器”连接起来，实现用户输入后自动生成结构化结果。"}
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human","{question}"),
    ("ai","定义：{definition}\n作用：{usage}\n例子：{example}"),
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一名面向初学者的 Python 和 LangChain 编程助教。这里的 LangServe 专指 LangChain 生态中的 LangServe。回答必须严格按照“定义：”“作用：”“例子：”三行输出。语言要通俗易懂，不要输出无关内容，不要猜测其他术语。"),
        few_shot_prompt,
        ("human","{question}")
    ]
)

llm = ChatOpenAI(
    model = "Qwen/Qwen2.5-7B-Instruct",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url = "https://api.siliconflow.cn/v1",
    temperature=0
)

chain = prompt | llm

if __name__ == "__main__":
    question = input("请输入你的问题：")
    response = chain.invoke({"question": question})
    print(response.content)

