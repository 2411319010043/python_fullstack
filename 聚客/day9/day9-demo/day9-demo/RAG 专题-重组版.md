# RAG 专题-重组版

## 1. 一句话总纲

`RAG = 先检索知识库，再基于检索结果生成回答。`

`语义搜索 = 找内容`
`RAG = 找内容 + 回答内容`

---

## 2. 主流程总图

`Loader -> Splitter -> Embedding -> Vector Store -> Retriever -> Prompt -> LLM`

一句话背诵：

`先读、先切、先存；再问、再找、再答。`

### 2.1 前期准备，只做一次
- 加载知识库
- 切分文档
- 文档向量化
- 存入向量库

### 2.2 每次提问都要做
- 用户问题向量化
- 检索相关片段
- 组装 Prompt
- 调用 LLM 生成回答

---

## 3. 核心角色

### 3.1 Loader
是什么：负责读取不同格式的文件。  
为什么：知识库可能是 `txt / csv / html / pdf`，不能都用同一种方式读取。  
一句话：`Loader 负责把文件读成 Document。`

### 3.2 Splitter
是什么：负责把长文档切成更小的块。  
为什么：整篇直接检索粒度太粗，不精准。  
一句话：`Splitter 负责把长文档切小。`

### 3.3 Embedding
是什么：把文本变成向量。  
为什么：只有变成向量，机器才能比较语义相似度。  
一句话：`Embedding 负责把文本变成可比较的坐标。`

### 3.4 Vector Store
是什么：存储向量、建索引、做检索的地方。  
为什么：只做 embedding 不够，还需要一个地方管理这些向量。  
一句话：`Vector Store 是向量仓库。`

### 3.5 Retriever
是什么：LangChain 提供的统一检索接口。  
为什么：方便后续统一调用，不直接操作底层向量库。  
一句话：`Retriever 负责查资料。`

### 3.6 Prompt
是什么：把“检索到的上下文 + 用户问题 + 规则”组织起来的模板。  
为什么：让 LLM 知道哪些是资料，哪些是问题，回答时要遵守什么规则。  
一句话：`Prompt 负责把材料喂给 LLM。`

### 3.7 LLM
是什么：负责理解上下文并生成最终回答。  
为什么：检索只负责找，真正自然语言回答还是要靠大模型。  
一句话：`LLM 负责组织最终回答。`

### 3.8 Tool
是什么：给 Agent 调用的工具形态。  
为什么：Agent 更适合调用 tool，而不是直接理解 retriever。  
一句话：`Tool 是把能力包装给 Agent。`

### 3.9 Memory
是什么：多轮对话记忆。  
为什么：让模型知道前面聊过什么。  
一句话：`Memory 负责记住聊天上下文。`

---

## 4. 易混概念

### 4.1 RAG 和语义搜索
- 语义搜索：只负责找最相似的原文片段
- RAG：先找，再交给 LLM 回答

一句话区分：  
`语义搜索只找，RAG 先找再答。`

### 4.2 Vector Store 和 Retriever
- `vectordb`：向量库本体，像仓库
- `retriever`：统一检索接口，像取货窗口

一句话区分：  
`vectordb 是仓库，retriever 是窗口。`

### 4.3 Retriever 和 Tool
- `retriever`：检索能力本身
- `tool`：把检索能力包装给 Agent 用

一句话区分：  
`Retriever 负责查，Tool 负责交给 Agent 调。`

### 4.4 session_state 和 memory
- `st.session_state["messages"]`：给前端页面显示聊天记录
- `memory`：给 LangChain / LLM 提供历史上下文

一句话区分：  
`session_state 负责前端显示，memory 负责模型上下文。`

### 4.5 msgs 和 memory
- `msgs`：存聊天记录的容器
- `memory`：把容器内容按 LangChain 方式提供给模型

一句话区分：  
`msgs 负责存，memory 负责用。`

### 4.6 create_documents 和 split_documents
- `create_documents([text])`：适合原始字符串
- `split_documents(docs)`：适合 Document 列表

一句话区分：  
`字符串用 create_documents，Document 列表用 split_documents。`

### 4.7 Agent 和 AgentExecutor
- `agent`：负责思考和决策
- `agent_executor`：负责真正执行工具调用和返回结果

一句话区分：  
`agent 负责想，executor 负责干。`

### 4.8 固定RAG 和 ReAct Agent
- 固定RAG：流程写死，必须先检索再回答
- ReAct Agent：流程交给模型决定，要不要调工具由模型判断

一句话区分：  
`固定RAG 是硬流程，ReAct Agent 是模型自己决定流程。`

---

## 5. 切分器总结

### 5.1 RecursiveCharacterTextSplitter
是什么：偏结构切分。  
特点：优先按段落、换行、标点等边界切。  
优点：稳定、简单、好调试。  
缺点：语义不一定最自然。  

一句话：  
`RecursiveCharacterTextSplitter 更偏格式和结构。`

### 5.2 SemanticChunker
是什么：偏语义切分。  
特点：先比较句子语义差异，再决定在哪里切。  
优点：更贴近语义。  
缺点：更重、更慢、调参更复杂。  

一句话：  
`SemanticChunker 更偏语义变化。`

---

## 6. Memory 速记

- `st.session_state["messages"]`：前端显示聊天记录
- `msgs = StreamlitChatMessageHistory()`：LangChain 存历史的容器
- `memory = ConversationBufferMemory(...)`：给模型读写历史的接口
- `{chat_history}`：Prompt 里历史记录的占位符

一句话背诵：

`前端看 session_state，LangChain 存 msgs，模型吃 memory，prompt 用 {chat_history} 占位。`

### 6.1 memory_key 是什么
是什么：历史记录在 prompt 里的变量名。  
为什么：要和 prompt 里的占位符一一对应。  
例子：prompt 里是 `{chat_history}`，那就写 `memory_key="chat_history"`。

### 6.2 output_key 是什么
是什么：最终回答在结果字典里的键名。  
为什么：memory 要知道把哪一项当作助手回复存回历史。  
例子：`response["output"]`，那就写 `output_key="output"`。

一句话背诵：

`memory_key 管历史放哪，output_key 管回答取哪。`

---

## 7. 最小代码骨架

### 7.1 固定 RAG 最小版

```python
loader = TextLoader(path, encoding="utf-8")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="xxx")
vectordb = Chroma.from_documents(splits, embeddings)

retriever = vectordb.as_retriever()
docs = retriever.invoke(query)

print(docs[0].page_content)
```

一句话：
`固定RAG = 先查，再答。`

### 7.2 Agent 版 RAG 最小版

```
tool = create_retriever_tool(retriever, "document_search", "用于检索文档")
tools = [tool]

base_prompt = PromptTemplate.from_template(base_prompt_template)
prompt = base_prompt.partial(instructions=instructions)

llm = ChatOpenAI(model="gpt-4o-mini", base_url=base_url, api_key=api_key)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": user_query})
print(response["output"])
```

一句话：
`Agent 版 RAG = 让模型自己决定要不要查。`

------

## 8. OCR 版 PDF 处理

### 8.1 为什么普通 PDF 有时读不到字

因为不是所有 PDF 都有文本层。
有些 PDF 本质上是图片，所以普通 `PyPDFLoader` 抽不到文字。

### 8.2 OCR 是什么

```
OCR = 把图片里的文字识别出来。
```

### 8.3 OCR 处理 PDF 的主线

1. 打开 PDF
2. 把每页转成图片
3. OCR 识别图片里的文字
4. 包装成 `Document`

一句话：
`PDF OCR = PDF 转图片 + 图片识字 + 包装成 Document。`

------

## 9. 检索策略补充

### 9.1 普通相似度检索是什么

是什么：只看“哪个片段和用户问题最像”，然后按相似度从高到低排序，取前 `k` 个返回。  
为什么：这是最基础、最直接的检索方式，简单、速度快。  
问题：如果前几名都来自同一个文档，或者内容很像，就容易重复，信息面不够广。  

示例：

```python
retriever = vectordb.as_retriever(search_kwargs={"k": 4})
```

这表示：用普通相似度检索，最后返回最相似的 `4` 个片段。  

一句话：  
`普通相似度检索 = 只按“像不像问题”排序。`

### 9.2 MMR 是什么

MMR 的全称是 `Maximum Marginal Relevance`，可以理解成“最大边际相关性检索”。  
它和普通相似度检索的区别是：它不只看“像不像问题”，还会看“和已经选中的片段是不是太重复”。  

它的目标是：
- 既要相关
- 也要尽量不重复

所以 MMR 更适合多文档场景。  
因为它能减少“返回的几个片段全都来自同一个文档，而且意思差不多”的情况。  
但要注意：MMR 不是“平均每个文件分一个结果”，它只是尽量让结果更多样。  

示例：

```python
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10},
)
```

一句话：  
`MMR = 先看相关，再尽量避免重复。`

### 9.3 fetch_k 是什么

`fetch_k` 不是最终返回数量，而是“先初步找出多少个候选片段”。  
MMR 会先从向量库里取出 `fetch_k` 个候选，再从这些候选里挑出最终的 `k` 个结果。  

可以这样理解：
- `fetch_k`：候选池大小
- `k`：最后真正返回给 LLM 的数量

比如：

```python
search_kwargs={"k": 4, "fetch_k": 10}
```

意思是：
1. 先找出 `10` 个比较相关的候选片段
2. 再从这 `10` 个里挑出 `4` 个“既相关、又不太重复”的片段

一句话：  
`fetch_k 决定先拿多少候选给 MMR 挑，k 决定最后真正返回多少。`

### 9.4 三者怎么区分

- 普通相似度检索：只按相似度排序，直接取前 `k` 个
- MMR：先看相关，再控制重复度
- `fetch_k`：不是最终返回数，而是给 MMR 提供候选池

一句话背诵：  
`普通检索是最像的直接拿，MMR 是最像的里面挑几个不那么重复的，fetch_k 是先准备多少候选。`

------## 9. 常见问题排查

### 9.1 如果回答不准，先查哪里？

先查 `Retriever 有没有找对`，再查 `Prompt / LLM 有没有答偏`。

### 9.2 如果知识库里明明有答案，但总检索不到

可能原因：

- 切分不合理
- embedding 模型不适合当前语言
- 向量库设置不合适
- retriever 参数不合适

### 9.3 如果上传多个文档，但总偏向某一份文档

可能原因：

- 问题太泛
- 某个文件 chunk 更多
- 普通相似度检索容易让同一文档占满前几名

优化方向：

- 调大 `k`
- 改成 `MMR`
- 针对“全库总结”单独做总结模式

### 9.4 如果 PDF 明明有内容，但系统说没有

先判断：

- 是不是扫描版 / 图片版 PDF
- 普通 loader 有没有抽出文字
- 如果抽出来全空，就要考虑 OCR

### 9.5 如果 Agent 报 parsing error

本质原因：模型没有按 `Thought / Action / Final Answer` 的固定格式输出。
说明：这不是知识库问题，而是 ReAct 格式解析问题。

------

## 10. 一句话背诵区

- `RAG = 先检索，再生成`
- `语义搜索只找，RAG 先找再答`
- `Loader 负责读，Splitter 负责切，Embedding 负责变向量`
- `Vector Store 是仓库，Retriever 是检索窗口`
- `Retriever 查资料，Tool 给 Agent 调，Memory 记聊天历史`
- `固定RAG 是硬流程，ReAct Agent 是模型自己决定流程`
- `写在 prompt 里的是要求，写在代码里的才是强制`
- `PDF 读不到字，不一定是检索差，可能是 loader 没抽到文本`
