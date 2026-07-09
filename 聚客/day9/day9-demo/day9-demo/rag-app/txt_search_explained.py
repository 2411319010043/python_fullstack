"""
# what：这是 txt_search.py 的教学版注释文件
# why：方便按 what / why / how 回顾 RAG 聊天应用每一段代码在做什么
# how：保留和原文件一致的主线结构，并补充更清楚的中文注释
"""

# what：导入 Streamlit，并给它起一个简短别名 st
# why：这个项目是一个网页聊天应用，需要用 Streamlit 来搭页面、收文件、收输入、显示输出
# how：使用 import streamlit as st，让后续可以用 st.title、st.chat_input 这类页面组件
import streamlit as st

# what：导入 tempfile
# why：用户上传的文件先是内存里的上传对象，不是磁盘真实文件，所以要先写入临时目录
# how：后面会用 tempfile.TemporaryDirectory() 创建临时目录
import tempfile

# what：导入 os
# why：需要拼接临时文件路径
# how：后面会用 os.path.join() 生成上传文件落盘后的真实路径
import os

# what：导入 LangChain 的对话记忆包装器
# why：我们希望 Agent 在多轮对话时能拿到 chat_history
# how：后面会把 Streamlit 的消息历史包装成 ConversationBufferMemory
from langchain_classic.memory import ConversationBufferMemory

# what：导入 Streamlit 专用的聊天历史容器
# why：要把 LangChain 用的聊天记录存进 Streamlit 的 session_state
# how：实例化 StreamlitChatMessageHistory() 后，底层会自动绑定到 session_state
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# what：导入文本文件加载器
# why：上传的是 txt 文件，后续要把它读成 LangChain 统一的 Document 结构
# how：后面会用 TextLoader(temp_filepath, encoding="utf-8")
from langchain_community.document_loaders import TextLoader

# what：导入 HuggingFace 向量模型封装器
# why：我们不依赖在线 embedding 接口，而是使用本地向量模型来做文档向量化
# how：后面会实例化 HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
from langchain_huggingface import HuggingFaceEmbeddings

# what：导入 Chroma 向量数据库
# why：切分后的文档要向量化并存入向量库，后面才能做检索
# how：后面会用 Chroma.from_documents(splits, embeddings)
from langchain_chroma import Chroma

# what：导入 Prompt 模板类
# why：我们要把“规则 + 工具格式 + 历史 + 当前问题”拼成 Agent 可用的完整提示词
# how：后面会用 PromptTemplate.from_template(base_prompt_template)
from langchain_core.prompts import PromptTemplate

# what：导入递归字符切分器
# why：上传的 txt 文本可能比较长，需要先切块后再向量化
# how：后面会实例化 RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# what：导入 ReAct Agent 和执行器
# why：这个例子不是固定 RAG，而是 Agent 版 RAG，所以要让 Agent 学会调工具
# how：后面用 create_react_agent(llm, tools, prompt) 创建 Agent，再用 AgentExecutor 真正执行
from langchain_classic.agents import create_react_agent, AgentExecutor

# what：导入 Streamlit 回调处理器
# why：我们想在页面里看到 Agent 的工具调用过程
# how：后面会把它放进 callbacks，让页面显示“Thought / Action / Observation”
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# what：导入聊天模型封装器
# why：最终回答还是要靠 LLM 生成
# how：后面会实例化 ChatOpenAI(model="gpt-4o-mini", ...)
from langchain_openai import ChatOpenAI

# what：设置网页的基础配置
# why：page_title 决定浏览器标签页标题，layout="wide" 让页面更宽一些
# how：调用 st.set_page_config(...)
st.set_page_config(page_title="Rag Agent", layout="wide")

# what：在网页正文里显示一个大标题
# why：让用户一打开页面就知道这个应用是干什么的
# how：调用 st.title("Rag Agent")
st.title("Rag Agent")

# what：在左侧边栏放一个 txt 文件上传组件
# why：这个 RAG 聊天应用的知识库来自用户上传的 txt 文件
# how：使用 st.sidebar.file_uploader(..., type=["txt"], accept_multiple_files=True)
uploaded_files = st.sidebar.file_uploader(
    label="上传txt文件", type=["txt"], accept_multiple_files=True
)

# what：判断用户有没有上传文件
# why：后面的加载、切分、向量化、建库都依赖上传文件，没有文件时没法继续
# how：如果 uploaded_files 为空，就提示并调用 st.stop() 阻止后续代码继续执行
if not uploaded_files:
    st.info("请先上传TXT文档。")
    st.stop()


# what：定义“构建 retriever”的函数
# why：加载、切分、向量化、建库这一套流程比较长，而且在 Streamlit 中属于重活，适合单独封装
# how：把上传文件传进来，函数最后返回一个 retriever
@st.cache_resource(ttl="1h")
def configure_retriever(uploaded_files):
    # what：准备一个空列表，用来装加载出来的所有 Document
    # why：用户可能上传多个 txt 文件，我们要把这些文件统一收集起来再切分
    # how：定义 docs = []
    docs = []

    # what：创建一个临时目录
    # why：Streamlit 上传的是“内存里的上传文件对象”，TextLoader 更适合读“磁盘上的真实文件路径”
    # how：用 tempfile.TemporaryDirectory() 生成临时目录
    temp_dir = tempfile.TemporaryDirectory(dir=r"D:\\")

    # what：遍历用户上传的每个文件
    # why：支持多文件上传，所以要一份份落盘、一份份加载
    # how：使用 for file in uploaded_files
    for file in uploaded_files:
        # what：拼出这个上传文件在临时目录中的真实路径
        # why：后面需要把上传内容写进这个路径，再交给 TextLoader
        # how：使用 os.path.join(temp_dir.name, file.name)
        temp_filepath = os.path.join(temp_dir.name, file.name)

        # what：把上传文件写入临时目录
        # why：先把“上传对象”变成“磁盘上的真实文件”，TextLoader 才能读取
        # how：用 open(..., "wb") 写入 file.getvalue()
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())

        # what：创建 txt 文件加载器
        # why：要把 txt 文件内容读成 LangChain 的 Document 结构
        # how：实例化 TextLoader(temp_filepath, encoding="utf-8")
        loader = TextLoader(temp_filepath, encoding="utf-8")

        # what：加载 txt 文件，并把结果合并到 docs 列表中
        # why：loader.load() 返回的是 Document 列表，所以这里要用 extend 而不是 append
        # how：调用 docs.extend(loader.load())
        docs.extend(loader.load())

    # what：创建递归切分器
    # why：单个 txt 文件可能很长，直接整篇向量化会让检索粒度太粗
    # how：设置 chunk_size=300，chunk_overlap=50
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    # what：把加载出来的 Document 列表再切成更小的块
    # why：后面向量检索要用更小、更适合匹配的 chunks
    # how：调用 text_splitter.split_documents(docs)
    splits = text_splitter.split_documents(docs)

    # what：实例化 embedding 模型
    # why：向量库建库前，必须先把文本切片变成向量
    # how：使用 HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # what：从切片直接创建 Chroma 向量库
    # why：这一步会同时做“切片向量化 + 存储 + 建立可检索结构”
    # how：调用 Chroma.from_documents(splits, embeddings)
    vectordb = Chroma.from_documents(splits, embeddings)

    # what：把向量库包装成统一检索接口
    # why：后续 LangChain 的 tool 和 agent 更喜欢接 retriever，而不是直接接 vectordb
    # how：调用 vectordb.as_retriever()
    retriever = vectordb.as_retriever()

    # what：返回 retriever
    # why：外层真正要用的是“可直接检索的接口”，不是底层向量库对象本身
    # how：return retriever
    return retriever


# what：根据当前上传文件，构建 retriever
# why：后面 tool、agent、问答流程都建立在 retriever 已经准备好的前提上
# how：调用 configure_retriever(uploaded_files)
retriever = configure_retriever(uploaded_files)

# what：初始化给前端显示用的聊天记录
# why：页面每次重跑时，仍然要能看见之前显示过的聊天内容
# how：把欢迎语写进 st.session_state["messages"]
if "messages" not in st.session_state or st.sidebar.button("清空聊天记录"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "您好，我是聚客AI助手，我可以查询文档"}
    ]

# what：把历史聊天记录画到页面上
# why：让用户能看到已经聊过的内容
# how：遍历 st.session_state.messages，逐条调用 st.chat_message(...).write(...)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# what：导入 retriever 工具构建函数
# why：我们要把 retriever 包成 Agent 能调用的 tool
# how：从 langchain_core.tools 导入 create_retriever_tool
from langchain_core.tools import create_retriever_tool

# what：创建“文档检索”工具
# why：让 Agent 能把“查知识库”当作一件可调用的工具来用
# how：传入 retriever、工具名、工具描述
tool = create_retriever_tool(
    retriever,
    "文档检索",
    "用于检索用户提出的问题，并基于检索到的文档内容进行回复。",
)

# what：把工具放进 tools 列表
# why：create_react_agent 需要接收一个工具列表
# how：tools = [tool]
tools = [tool]

# what：创建一个给 LangChain 用的聊天历史容器
# why：Agent 和 Memory 需要一个地方保存多轮对话消息
# how：实例化 StreamlitChatMessageHistory()，底层会绑定到 Streamlit 的 session_state
msgs = StreamlitChatMessageHistory()

# msgs 是原始记录本，ConversationBufferMemory 是翻译器，负责把记录本翻译成 Agent 能直接使用的记忆格式。
# what：创建一个对话记忆包装器，ConversationBufferMemory 就是在把 msgs 包装成 LangChain 认得的 memory 接口
# why：LLM/Agent 需要一个符合 memory 接口的对象来拿 chat_history
# how：把 msgs 传给 chat_memory，再约定 history 变量名叫 chat_history
memory = ConversationBufferMemory(
    chat_memory=msgs,
    return_messages=True,
    memory_key="chat_history",
    output_key="output",
)

# what：定义 Agent 的行为规则
# why：我们要约束 Agent “先查文档再回答，查不到就说不知道”
# how：写一段 system-style 的自然语言指令
instructions = """您是一个设计用于查询文档来回答问题的代理。
您可以使用文档检索工具，并基于检索内容来回答问题。
您可能不查询文档就知道答案，但是您仍然应该查询文档来获得答案。
如果您从文档中找不到任何信息用于回答问题，则只需返回“抱歉，这个问题我还不知道。”作为答案。
"""

# what：定义 ReAct Agent 的基础提示词模板
# why：除了内容规则外，Agent 还需要知道“工具调用格式”、“历史消息放哪”、“用户输入放哪”
# how：用多行字符串写出完整 prompt 模板，并留出 {instructions}、{tools}、{chat_history} 等占位符
base_prompt_template = """
{instructions}

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: {input}
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""

# what：把原始字符串模板转成 PromptTemplate 对象
# why：LangChain 需要正式的模板对象，后面才能注入变量
# how：调用 PromptTemplate.from_template(base_prompt_template)
base_prompt = PromptTemplate.from_template(base_prompt_template)

# what：把 instructions 填进 prompt
# why：把“通用骨架”和“这次具体规则”分开写，更清晰、更方便复用
# how：调用 base_prompt.partial(instructions=instructions)
prompt = base_prompt.partial(instructions=instructions)

# what：实例化聊天模型
# why：最终回答还是要靠 LLM 生成
# how：使用兼容 OpenAI 接口的 ChatOpenAI，调用中转站里的 gpt-4o-mini
llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="http://192.168.1.56:3000/v1",
    api_key="YOUR_API_KEY",
)

# what：创建 ReAct Agent
# why：把 llm、tools、prompt 组合成一个“会按规则用工具”的代理
# how：调用 create_react_agent(llm, tools, prompt)
agent = create_react_agent(llm, tools, prompt)

# what：创建 Agent 执行器
# why：真正跑 Agent 还需要 memory、日志显示、错误处理这些执行层配置
# how：把 agent、tools、memory 等交给 AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
)

# what：创建聊天输入框
# why：让用户可以在网页里直接提问
# how：调用 st.chat_input(...)
user_query = st.chat_input(placeholder="请开始提问吧!")

# what：处理用户输入并生成回答
# why：这是整个网页聊天应用的最终入口
# how：先显示用户消息，再调用 agent_executor.invoke(...)，最后保存并显示助手回答
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        # what：创建 Streamlit 回调处理器
        # why：在页面中展示 Agent 的工具调用过程
        # how：实例化 StreamlitCallbackHandler(st.container())
        st_cb = StreamlitCallbackHandler(st.container())

        # what：准备回调配置
        # why：让 invoke 执行时把中间过程同步显示到页面
        # how：把回调处理器放进 callbacks 列表
        config = {"callbacks": [st_cb]}

        # what：调用执行器，正式跑 Agent
            # agent_executor.invoke(...) = 让整个 Agent 系统正式处理这次提问。
        # why：让 Agent 能结合 memory、prompt、tool 和 llm 来完成一轮问答
        # how：调用 agent_executor.invoke({"input": user_query}, config=config)
        response = agent_executor.invoke({"input": user_query}, config=config)

        # what：把助手回答保存到前端聊天记录里
        # why：页面后续重跑时还能继续显示这条回答
        # how：往 st.session_state.messages 里追加 assistant 消息
        st.session_state.messages.append(
            {"role": "assistant", "content": response["output"]}
        )

        # what：把最终回答显示到页面
        # why：让用户看到整理后的中文答案
        # how：调用 st.write(response["output"])
        st.write(response["output"])
