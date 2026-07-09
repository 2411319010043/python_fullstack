# what: 导入 `os` 模块，用来读取环境变量、拼接路径等。
# why: 这个项目要从 `.env` 或系统环境里读取 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 这些配置。
# how: 通过 `os.getenv(...)` 读取环境变量，通过 `os.path.join(...)` 处理路径。
import os

# what: 导入 `tempfile` 模块，用来创建临时目录。
# why: Streamlit 上传的文件一开始在内存里，而 `TextLoader` 更适合读取已经落到磁盘上的文件。
# how: 通过 `tempfile.TemporaryDirectory(...)` 创建一个临时文件夹，把上传文件先写进去。
import tempfile

# what: 导入 `streamlit`，这是一个快速搭建网页界面的 Python 框架。
# why: 我们这份作业要做成一个“能上传文档、能提问、能看到回答”的网页聊天助手。
# how: 统一写成 `import streamlit as st`，后面通过 `st.xxx(...)` 调用它的页面组件。
import streamlit as st

# what: 导入 `load_dotenv`，用于读取 `.env` 文件里的配置。
# why: `.env` 只是一个文本文件，不会自动进入 Python 环境变量，所以要手动加载。
# how: 先 `from dotenv import load_dotenv`，再执行一次 `load_dotenv()`。
from dotenv import load_dotenv

# what: 导入提示词模板类 `PromptTemplate`。
# why: Agent 需要一份固定格式的提示词模板，告诉大模型该如何思考、何时调用工具、何时输出最终答案。
# how: 通过 `PromptTemplate.from_template(...)` 把一个带占位符的长字符串变成可复用模板。
from langchain_core.prompts import PromptTemplate

# what: 导入 `TextLoader`，它是用来读取 txt 文本文件的加载器。
# why: 用户上传的是 txt 文档，我们要先把 txt 文件读成 LangChain 能识别的 `Document` 对象。
# how: 传入 txt 文件路径和编码方式，再调用 `loader.load()` 即可。
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import BSHTMLLoader
from langchain_community.document_loaders import PyPDFLoader

# what: 导入递归字符切分器 `RecursiveCharacterTextSplitter`。
# why: 原始文档可能太长，不能整篇直接丢进向量库，所以要先切成更小的片段方便检索。
# how: 实例化时设置 `chunk_size` 和 `chunk_overlap`，再调用 `split_documents(...)` 切分。
from langchain_text_splitters import RecursiveCharacterTextSplitter

# what: 导入 HuggingFace 的向量模型封装 `HuggingFaceEmbeddings`。
# why: 文本要先变成向量，后面才能做语义相似度检索。
# how: 指定模型名，例如 `"sentence-transformers/all-MiniLM-L6-v2"` 来实例化。
from langchain_huggingface import HuggingFaceEmbeddings

# what: 导入 `Chroma` 向量数据库。
# why: 只做 embedding 还不够，我们还需要一个地方存向量、建索引、做检索。
# how: 通过 `Chroma.from_documents(...)` 把切分后的文档直接写进向量库。
from langchain_chroma import Chroma

# what: 导入 `ChatOpenAI` 聊天模型封装。
# why: 检索只负责找资料，最终自然语言回答还是要交给大模型来生成。
# how: 传入 `model`、`base_url`、`api_key` 来实例化聊天模型。
from langchain_openai import ChatOpenAI

# what: 导入 `create_retriever_tool`，它能把 retriever 包装成 tool。
# why: Agent 自己不会直接理解 retriever 是什么，所以要把检索能力包装成“工具”的形态给 Agent 使用。
# how: 传入 `retriever`、工具名称、工具描述，就能得到一个可供 Agent 调用的 tool。
from langchain_core.tools import create_retriever_tool

# what: 导入 `create_react_agent` 和 `AgentExecutor`。
# why: `create_react_agent` 负责创建 Agent，大脑逻辑在这里；`AgentExecutor` 负责真正执行 Agent。
# how: 先用 `create_react_agent(...)` 生成 Agent，再把它交给 `AgentExecutor(...)` 来跑。
from langchain_classic.agents import AgentExecutor, create_react_agent

# what: 导入 `StreamlitChatMessageHistory`，它是 LangChain 适配 Streamlit 的聊天历史容器。
# why: Agent 的 memory 需要一个能存历史消息的容器，这个类正好负责“存历史”。
# how: 实例化后传给 `ConversationBufferMemory(chat_memory=...)` 使用。
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# what: 导入 `StreamlitCallbackHandler`，它是 Streamlit 专用的回调处理器。
# why: 这样 Agent 在思考、调用工具、得到观察结果时，可以把过程显示在网页上，方便调试和学习。
# how: 在调用 `agent_executor.invoke(...)` 时，通过 `config={"callbacks": [st_cb]}` 传进去。
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# what: 导入 `ConversationBufferMemory`，它是最基础的对话记忆类。
# why: 我们希望模型能看到之前几轮聊天内容，而不是每次回答都像第一次见你。
# how: 把聊天历史容器传进去，再设置 `memory_key="chat_history"`，供 prompt 使用。
from langchain_classic.memory import ConversationBufferMemory

import fitz
from rapidocr_onnxruntime import RapidOCR
from langchain_core.documents import Document
 # PDF -> 每页变图片 -> OCR识字 -> 包装成Document
def ocr_pdf_to_documents(pdf_path):
    # what: 创建一个空列表，用来存放 OCR 识别后的 Document 对象
    # why: 后面每识别完一页 PDF，就要往里面放一个 Document
    # how: 先定义一个普通列表，名字叫 documents
    documents = []
    # what: 创建 OCR 识别器。
    # why: 后面真正识别图片里文字的就是它。
    # how: 实例化一次就够了。
    ocr_engine = RapidOCR()
    # what：打开 PDF。
    # why: 你得先拿到整本 PDF，才能一页一页处理。
    # how: 把文件路径传给 fitz.open(...)。
    pdf_document = fitz.open(pdf_path)
    # what: 遍历 PDF 转出来的每一页图片
    # why: 多页 PDF 需要一页一页做 OCR 识别
    # how: enumerate(..., start=1) 能同时拿到页码和图片对象
    for page_num in range(len(pdf_document)):
        # what：取当前页
        page = pdf_document[page_num]
        # what：把当前页渲染成图像
        pix = page.get_pixmap()
        # what：把图像变成 png 字节
        image_bytes = pix.tobytes("png")

        # what：对当前页图片做 OCR。
        # why: 把图片里的字识别出来。
        # how: 把图片字节交给 ocr_engine(...)。
        result, _ = ocr_engine(image_bytes)

        text = ""
        if result:
            # what: 把 OCR 结果拼成一整段文本。
            # why：OCR 返回的不是一个大字符串，而是很多识别片段。
            # how：把每一小段识别文字拿出来，再用换行拼接。
            text = "\n".join([line[1] for line in result])

        doc = Document(
            page_content=text,
            metadata={"source": pdf_path, "page":page_num + 1}
        )
        documents.append(doc)

    return documents

# what: 调用 `load_dotenv()`，把 `.env` 文件中的变量加载到当前程序环境里。
# why: 如果不先加载，`os.getenv("OPENAI_API_KEY")` 很可能读不到你写在 `.env` 里的内容。
# how: 这一行通常放在真正读取环境变量之前执行一次就够了。
load_dotenv()

# what: 设置 Streamlit 页面基础配置。
# why: 这样网页标签标题更清楚，页面布局也更宽，更适合聊天和展示文档检索过程。
# how: `page_title` 控制浏览器页签标题，`layout="wide"` 让页面使用宽布局。
st.set_page_config(page_title="RAG Agent", layout="wide")

# what: 在页面顶部显示大标题。
# why: 让用户一打开网页就知道这是一个什么应用。
# how: 通过 `st.title(...)` 直接显示主标题文字。
st.title("RAG Agent")

# what: 在侧边栏创建一个文件上传组件。
# why: 这个项目是“基于用户上传文档”的 RAG，所以第一步必须先让用户上传知识库文件。
# how: `label` 是展示文字，`type=["txt"]` 限制只能传 txt，`accept_multiple_files=True` 允许一次传多个文件。
uploaded_files = st.sidebar.file_uploader(
    label="上传文档",
    type=["txt","pdf","csv","html"],
    accept_multiple_files=True,
)

# what: 判断用户是否还没有上传文件。
# why: 没有知识库就没法做后面的切分、向量化、检索，所以这里要先拦住。
# how: `uploaded_files` 为空时进入这个分支。
if not uploaded_files:
    # what: 在页面上给用户一个提示。
    # why: 比直接报错更友好，能明确告诉用户下一步该做什么。
    # how: `st.info(...)` 会显示一个蓝色的信息提示框。
    st.info("请先上传知识库文档（支持 TXT / PDF / CSV / HTML）。")

    # what: 立即停止当前这次 Streamlit 脚本执行。
    # why: 如果没有文件还继续往下跑，后面的建库和检索逻辑都会报错。
    # how: `st.stop()` 会终止本轮页面脚本运行。
    st.stop()


# what: 给“构建 retriever”这个重操作函数加缓存。
# why: Streamlit 每次交互都会重新执行脚本，如果不缓存，切分、向量化、建库会反复重跑，非常浪费时间。
# how: `ttl="1h"` 表示这份缓存默认保留 1 小时。
@st.cache_resource(ttl="1h")
def configure_retriever(uploaded_files):
    # what: 创建一个空列表，用来收集所有加载出来的 `Document` 对象。
    # why: 用户可能一次上传多个 txt 文件，所以要先把多个文件的文档都汇总起来。
    # how: 后面通过 `docs.extend(loader.load())` 往这个列表里追加。
    docs = []

    # what: 创建一个临时目录对象。
    # why: 上传文件最开始在内存里，而 `TextLoader` 需要文件路径，所以要先找个临时目录落盘。
    # how: `temp_dir.name` 就是这个临时目录对应的真实路径。
    temp_dir = tempfile.TemporaryDirectory()

    # what: 遍历用户上传的每一个文件。
    # why: 因为我们允许多文件上传，所以要逐个处理。
    # how: `uploaded_files` 里的每个 `file` 都是 Streamlit 上传文件对象。
    for file in uploaded_files:
        # what: 生成“临时目录 + 原始文件名”的完整路径。
        # why: 只有先拼出真实路径，后面才能把内存里的文件内容写入磁盘。
        # how: `temp_dir.name` 是临时目录路径，`file.name` 是用户上传文件的名字。
        temp_filepath = os.path.join(temp_dir.name, file.name)

        # what: 以二进制写入模式打开一个临时文件。
        # why: 上传组件拿到的是文件字节内容，写回磁盘时应该用二进制方式更稳妥。
        # how: `"wb"` 表示 write binary。
        with open(temp_filepath, "wb") as f:
            # what: `file.getvalue()` 用来取出上传文件的真实字节内容。
            # why: `file` 不是普通路径字符串，它是 Streamlit 的上传文件对象，所以要先把内容取出来。
            # how: 取出来后交给 `f.write(...)` 写进临时文件。
            f.write(file.getvalue())

        file_name = file.name.lower()
        
        if file_name.endswith(".txt"):
            # what: 用 `TextLoader` 实例化一个 txt 加载器。
            # why: 我们已经把上传文件落到磁盘了，现在就可以按“本地 txt 文件”的方式读取它。
            # how: 传入文件路径和 `utf-8` 编码。
            loader = TextLoader(temp_filepath, encoding="utf-8")
        elif file_name.endswith(".csv"):
            loader = CSVLoader(temp_filepath, encoding="utf-8")
        elif file_name.endswith(".html"):
            loader = BSHTMLLoader(temp_filepath, open_encoding="utf-8")
        elif file_name.endswith(".pdf"):
            loader = PyPDFLoader(temp_filepath)
            pdf_docs = loader.load()

            if all(not doc.page_content.strip() for doc in pdf_docs):
                pdf_docs = ocr_pdf_to_documents(temp_filepath)
            
            docs.extend(pdf_docs)
            continue
        else:
            st.warning(f"暂不支持文件类型：{file.name}")
            continue
        # what: 把这个 txt 文件加载出来的 `Document` 列表追加到总文档列表中。
        # why: `loader.load()` 返回的是列表，所以这里用 `extend`，不是 `append`。
        # how: `extend` 会把列表中的每个 `Document` 逐个加入 `docs`。
        docs.extend(loader.load())

    # what: 实例化递归字符切分器。
    # why: 长文档直接整块进向量库，检索粒度太粗，不利于精准找到和问题最相关的片段。
    # how: `chunk_size=300` 表示每块大约 300 个字符，`chunk_overlap=20` 表示相邻块重叠 20 个字符。
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)

    # what: 把 `Document` 列表切分成更小的 `Document` 片段列表。
    # why: 只有先切分，后面的向量库检索才能更细粒度、更准确。
    # how: 因为现在手里是 `Document` 列表，所以用 `split_documents(docs)`。
    splits = text_splitter.split_documents(docs)

    # what: 实例化向量模型。
    # why: 文档片段和用户问题都要变成向量，后面才能比较语义相似度。
    # how: 这里使用本地 HuggingFace 模型，并设置 `local_files_only=True`，避免联网下载。
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/LaBSE",
        model_kwargs={"local_files_only": True},
    )

    # what: 用切分后的文档直接创建 Chroma 向量库。
    # why: 这一步会同时完成“文档向量化 + 存入向量库 + 建立索引”。
    # how: 第一个参数是切分后的文档列表，第二个参数是 embedding 模型。
    vectordb = Chroma.from_documents(splits, embeddings)

    # what: 把底层向量库包装成 LangChain 统一的检索接口 `retriever`。
    # why: 后面不想直接操作底层向量库细节，而是希望用统一接口来“传入问题，返回相关文档”。
    # how: 通过 `vectordb.as_retriever()` 得到 retriever。
    retriever = vectordb.as_retriever(
        # what：把普通检索改成 MMR 检索。
        # why：你原来 k=1 只拿 1 段内容，太容易被某一个文档“抢占”。多文档一起上传时，经常只看到一份文档的声音。
        # how：k=4：最终返回 4 个片段给 Agent,fetch_k=10：先粗选 10 个候选，再从里面挑“既相关、又别太重复”的 4 个
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10})

    # what: 返回已经配置好的检索器。
    # why: 外部主流程只关心“拿到一个可检索的 retriever”，不关心内部建库细节。
    # how: 调用这个函数时，接收返回值即可。
    return retriever


# what: 调用上面的函数，真正构建出 retriever。
# why: 后面不管是包装 tool，还是给 Agent 检索知识库，都要先拿到 retriever。
# how: 把用户刚刚上传的文件列表 `uploaded_files` 传进去。
retriever = configure_retriever(uploaded_files)

# what: 创建一个侧边栏“清空聊天记录”按钮，并接收它本轮是否被点击。
# why: 把按钮结果单独放进变量里，会比直接写进 `if` 条件更清楚，也方便后面同时清理前端记录和 memory。
# how: 用户这一轮点击按钮时，`clear_chat` 会是 `True`。
clear_chat = st.sidebar.button("清空聊天记录")

# what: LangChain 用的聊天记录容器。
# why: 它负责替 LangChain 保存聊天历史，供 memory 使用。
# how: 直接实例化 `StreamlitChatMessageHistory()`。
msgs = StreamlitChatMessageHistory()

# what: 判断是否第一次进入页面，或者用户点击了“清空聊天记录”按钮。
# why: 第一次进入时要初始化历史消息；如果用户点击清空，也要重新初始化。
# how: `st.session_state` 是 Streamlit 保存页面状态的地方，`clear_chat` 是按钮状态。
if "messages" not in st.session_state or clear_chat:
    # what: 把 LangChain 侧保存的历史消息也一起清空。
    # why: 只清前端页面不清 memory，会出现“页面空了，但模型还记得上一轮聊天”的错位。
    # how: 调用 `msgs.clear()`，把聊天历史容器里的旧消息删掉。
    msgs.clear()

    # what: 给前端页面显示聊天记录
    # why: 页面上总得先有一句欢迎语，否则一打开会显得很空。
    # how: 这里放的是一个列表，列表里的每个元素都是一条消息字典。
    st.session_state["messages"] = [
        {"role": "assistant", "content": "您好，我是 AI 助手，我可以查询文档。"}
    ]

# what: 遍历页面状态里已经保存的聊天记录。
# why: Streamlit 每次交互会重新跑脚本，所以要把历史消息重新渲染一遍。
# how: `msg["role"]` 决定消息是谁说的，`msg["content"]` 是消息正文。
for msg in st.session_state.messages:
    # what: 在页面上渲染一条聊天消息。
    # why: 这样用户才能在界面上看到完整对话历史。
    # how: `st.chat_message(...).write(...)` 是 Streamlit 聊天界面的常见写法。
    st.chat_message(msg["role"]).write(msg["content"])

# what: 把 retriever 包装成一个给 Agent 用的检索工具。
# why: Agent 不会直接“天然理解 retriever”，但它会理解“我现在有一个叫文档检索的工具可以调用”。
# how: 传入 retriever、工具名、工具描述，返回一个 tool 对象。
tool = create_retriever_tool(
    retriever,
    "文档检索",
    "用于检索用户问题相关的文档片段，必须先查文档，再根据文档内容回答。",
)

# what: 把工具放进列表里。
# why: Agent 一般接收的是一个工具列表，即使现在只有一个工具，也要按列表形式传入。
# how: 用方括号把 `tool` 包起来即可。
tools = [tool]

# what: 把“历史消息容器”包装成 memory 接口。
# why: `msgs` 只负责存消息，而 `memory` 负责把这些消息按 LangChain 的 memory 接口提供给 Agent。
# how: `memory_key="chat_history"` 要和 prompt 里的 `{chat_history}` 占位符对应起来。
memory = ConversationBufferMemory(
    # what：历史实际存在哪。
    # why：总得有个容器装消息。
    # how：传入 StreamlitChatMessageHistory()。
    chat_memory=msgs,
    return_messages=True,
    # what：历史记录变量名。
    # why：要和 prompt 里的 {chat_history} 对上。
    # how：prompt 里写什么，这里就写什么。
    memory_key="chat_history",
    # what：助手回答存回 memory 时，对应结果字典里的哪个键。
    # why：invoke() 返回的是字典，memory 要知道哪一项是最终回答。
    # how：Agent 最终回答通常在 response["output"]，所以这里写 output。
    output_key="output",
)

# what: 定义一段针对当前作业的行为约束说明。
# why: Agent 默认有一定自由度，所以要明确告诉它“必须先查文档，再回答；找不到就说不知道”。
# how: 把这些规则写成字符串，后面注入 prompt。
instructions = """你是一个严格基于文档检索结果回答问题的助手。

你必须遵守下面规则：
1. 每次回答前，必须先调用一次“文档检索”工具。
2. 你只能根据检索到的文档内容回答，不能使用你自己的常识、背景知识或现实世界知识。
3. 如果文档中没有答案，就明确回答“根据文档，无法找到答案”。
4. 即使你知道文档内容可能不准确，也不能纠正文档，只能按文档回答。
5. 你输出时，必须严格使用下面规定的英文标签：
Thought:
Action:
Action Input:
Observation:
Final Answer:
6. 不要把这些标签写成中文，不要省略任何一个必须字段。
7. 如果你已经决定调用工具，就必须同时输出：
Thought:
Action:
Action Input:
不能只写 Thought。"""

# what: 定义 Agent 的基础提示词模板。
# why: ReAct Agent 需要固定的提示词格式，告诉模型工具有哪些、如何写 Thought / Action / Observation / Final Answer。
# how: 用一个带占位符的大字符串来写，后面再交给 `PromptTemplate.from_template(...)`。
base_prompt_template = """
{instructions}

You have access to the following tools:
{tools}

You must always call a tool before giving the final answer.

If you need to use a tool, you MUST output exactly in this format:

Thought: I should search the documents first.
Action: one of [{tool_names}]
Action Input: {input}

After the tool returns a result, you MUST continue in this format:

Observation: the tool result
Thought: I now know the answer.
Final Answer: your final answer here

If the document does not contain the answer, you MUST still give the final answer in this format:

Thought: I now know the answer.
Final Answer: 根据文档，无法找到答案。

Important rules:
1. The labels Thought, Action, Action Input, Observation, Final Answer must stay in English.
2. Do not omit Action after Thought when using a tool.
3. Do not output extra format explanations.
4. Do not answer directly before using the tool.
5. Your final answer must be based only on the retrieved document content.
6. If the observation already contains a direct answer, output Final Answer immediately.
7. Never call the same tool twice with the same input.

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""

# what: 把原始字符串模板转换成 LangChain 的提示词模板对象。
# why: 只有变成模板对象后，后面才能安全地做变量注入和部分填充。
# how: 调用 `PromptTemplate.from_template(base_prompt_template)`。
base_prompt = PromptTemplate.from_template(base_prompt_template)

# what: 先把 `instructions` 这部分固定注入到模板里。
# why: 这样后面创建 Agent 时，就不用每次手动再传一次这段规则说明。
# how: `partial(instructions=instructions)` 的意思是先把这个占位符填好。
prompt = base_prompt.partial(instructions=instructions)

# what: 从环境变量中读取模型名。
# why: 这样你以后要切换模型时，不用改代码，只改 `.env` 或系统环境变量就行。
# how: 如果环境里没配，就默认用 `"gpt-4o-mini"`。
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# what: 从环境变量中读取 OpenAI 兼容接口的 `base_url`。
# why: 你现在用的是中转或兼容接口，不一定走官方默认地址，所以这里要可配置。
# how: 如果环境里没配，就用你之前常用的默认地址。
openai_base_url = os.getenv("OPENAI_BASE_URL", "http://192.168.1.56:3000/v1")

# what: 从环境变量中读取 API Key。
# why: 没有 key 就没法真正调用聊天模型。
# how: 先读取，再 `strip()` 去掉首尾空格，避免看起来有值其实全是空白字符。
openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()

# what: 判断 API Key 是否为空。
# why: 如果 key 没读到，后面一调用模型就会报认证错误，所以这里提前拦截更容易排查。
# how: 空字符串在 Python 里会被判定为 False。
if not openai_api_key:
    # what: 在页面上提示用户先配置 API Key。
    # why: 这样用户能立刻知道问题不是代码逻辑，而是环境配置。
    # how: 用 `st.error(...)` 显示错误提示框。
    st.error("请先在 `.env` 或系统环境变量中配置 OPENAI_API_KEY。")

    # what: 停止本轮脚本执行。
    # why: 没有 key 继续往下创建 LLM 只会报错。
    # how: 直接调用 `st.stop()`。
    st.stop()

# what: 实例化聊天大模型。
# why: Agent 虽然有工具，但真正的思考、决策、组织回答还是要靠 LLM。
# how: 把模型名、接口地址、密钥都传进去。
llm = ChatOpenAI(
    model=openai_model,
    base_url=openai_base_url,
    api_key=openai_api_key,
)

# what: 创建 ReAct 风格的 Agent。
# why: ReAct Agent 会根据 prompt 判断是否要调用工具，再根据工具结果组织最终回答。
# how: 把 `llm`、`tools`、`prompt` 一起传给 `create_react_agent(...)`。
agent = create_react_agent(llm, tools, prompt)

# what: 创建 Agent 执行器。
# why: Agent 本身更像“大脑”和“规则”，真正负责执行的是 `AgentExecutor`。
# how: 把 Agent、工具、memory 等配置交给它。
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=2,
    early_stopping_method="generate",
)

# what: 在页面底部创建一个聊天输入框。
# why: 用户总得有地方输入自己的问题。
# how: 用户输入后，返回值会存到 `user_query` 变量里；如果这轮没输入，就会是空值。
user_query = st.chat_input(placeholder="请开始提问吧！")

# what: 判断用户这一轮是否真的输入了问题。
# why: 只有用户输入了内容，才需要触发后面的提问、检索、回答流程。
# how: `user_query` 非空时进入分支。
if user_query:
    # what: 先把用户消息追加到页面状态中的聊天记录里。
    # why: 这样下一次脚本重跑时，这条用户消息还能继续显示在页面上。
    # how: 往 `st.session_state["messages"]` 这个列表末尾追加一个字典。
    st.session_state.messages.append({"role": "user", "content": user_query})

    # what: 立即把用户刚输入的消息显示到聊天页面上。
    # why: 提升交互体验，让页面马上有反馈。
    # how: 通过 `st.chat_message("user").write(user_query)` 渲染。
    st.chat_message("user").write(user_query)

    # what: 创建一块“助手消息区域”。
    # why: 后面 Agent 的思考过程和最终答案都要显示在这块区域里。
    # how: 使用 `with st.chat_message("assistant"):` 上下文管理器。
    with st.chat_message("assistant"):
        # what: 创建一个 Streamlit 回调处理器。
        # why: 这样 Agent 的 Thought、Action、Observation 等中间过程可以在页面里实时展示。
        # how: 把一个容器传进去，让它知道往哪里渲染。
        st_cb = StreamlitCallbackHandler(st.container())

        # what: 组织调用 Agent 时要用到的配置字典。
        # why: LangChain 的 `invoke(...)` 可以通过 `config` 接收回调等运行配置。
        # how: 这里把刚创建的回调处理器放到 `callbacks` 里。
        config = {"callbacks": [st_cb]}

        # what: 真正调用 Agent 执行一次“提问 -> 检索 -> 回答”的完整流程。
        # why: 这是整个项目最核心的一步。
        # how: 把用户问题作为 `{"input": user_query}` 传入，再把回调配置一起传入。
        response = agent_executor.invoke({"input": user_query}, config=config)

        # what: 把助手的最终回答追加到页面状态中的聊天记录里。
        # why: 这样页面刷新或下次提问时，这条回答还会保留下来。
        # how: 从 `response["output"]` 里取出最终回答文本。
        st.session_state.messages.append(
            {"role": "assistant", "content": response["output"]}
        )

        # what: 把最终回答显示到页面上。
        # why: 用户最终真正关心的是这里的结果。
        # how: 直接 `st.write(response["output"])` 即可。
        st.write(response["output"])
