# RAG 专题

## 1. RAG 是什么？它和语义搜索有什么区别？

`RAG `是`检索增强生成`。它会先从外部知识库里检索出和问题最相关的内容，再把这些内容连同用户问题一起交给 `LLM` 生成最终回答。

`语义搜索`只负责“找”，通常返回的是最相似的原始文本片段。

```
语义搜索 = 找内容
RAG = 先找内容，再基于内容回答
```

## 2. RAG 为什么比直接问大模型更靠谱？

1. `有外部知识依据`

   不是只靠大模型脑子里“记得什么”，而是先去知识库里找相关内容，再回答，所以更有依据。

2. `能减少幻觉`

   因为回答不是凭空生成，而是基于检索给到的材料做生成，所以通常会更稳，更可控。

```
RAG 更靠谱，是因为它不是裸问 LLM，而是先查资料，再根据资料回答。
```

## 3. Loader 在 RAG里是干什么的？

`Loader `负责读取不同格式的文件，并把它们转换成后续流程能处理的`Document`.

## 4. 为什么 RAG 里需要 Splitter?

`Splitter` 负责把长文档切成更适合检索的小块，这样检索更精准，返回给 LLM 的上下文也更合适。

## 5. RecursiveCharacterTextSplitter 是什么？

`RecursiveCharacterTextSplitter `是一种偏“结构化”的切分器，优先按段落、换行、空格、标点这些边界来切分文本。

## 6. SemanticChunker 是什么？

`SemanticChunker `是一种偏“语义化”的切分器，它更关注语义是否发生变化，再决定在哪里切开。

## 7. Embedding 在 RAG 里是干什么的？

`Embedding `负责把文本转换成向量，方便机器用数学方法比较文本之间的语义相似度。

## 8. Vector Store 是什么？

`Vector Store` 负责存储向量、建立索引，并提供相似度检索能力，是向量化数据的“仓库”。

## 9. Retriever 是什么？

`Retriever `是 LangChain 提供的统一检索接口，用来从向量库中找出和用户问题最相关的文档片段。

## 10. Tool 是什么？

`Tool `是给 `Agent `调用的工具形态，本质上是把某种能力包装起来，让 Agent 决定什么时候使用它。

## 11. Memory 是什么？

`Memory ` 负责记录多轮对话历史，让系统知道前面聊了什么，但它不能替代知识检索。

## 12. 为什么说 Memory 不能替代 Retriever?

因为 Memory 记得是聊天上下文，Retriever 查的是外部知识库，它们负责的不是同一种“记忆”。

## 13. 一句话怎么区分Retriever、Tool 、Memory ？

`Retriever `负责查资料，`Tool `负责把能力交给 Agent 调用，`Memory  `负责记住聊天上下文。

# RAG 完整流程问答笔记

## 1. 一个最基础的 RAG 流程有哪几步？

通常是 `Loader 加载文档 -> Splitter 切分文档 -> Embedding 向量化 -> 存入 Vector Store -> 用户提问 -> Retriever 检索相关片段 -> 组装 Prompt -> LLM 生成回答`。

## 2. 哪些步骤是前期准备，只做一次？

`加载知识库、切分文档、文档向量化、存入向量库` 这些通常只做一次。

## 3. 哪些步骤是每次用户提问都要重新做？

`问题向量化、检索相关片段、组装Prompt、调用 LLM 回答`这些每次都要做。

## 4. 为什么不能把整个知识库直接丢给 LLM？

因为这样会`浪费 token、上下文太长、重点不突出、容易答偏`。

## 5. 为什么文档切完以后要做 Embedding，再存入 Vector Store?

因为 `Embedding `负责把文本变成可比较的向量，`Vector Store` 负责把这些向量存起来、建索引、方便检索。

## 6. 为什么用户问题也要向量化？

因为只有把问题也变成向量，才能和向量库里的文档向量做相似度比较。

## 7. Retriever 检索时，找到到底是什么？

找的是`和用户问题语义最接近的文档片段`

## 8. Retriever 返回的是向量还是原始文档？

返回的是`原始 Document`，因为后面要把可读文本交给它，而不是把一堆数字交给它。

## 9. 为什么 LLM 不能直接看向量回答？

因为向量本质上是 `一组数字坐标`，它适合做相似度计算，不适合直接拿来给 LLM 理解语义。

## 10. 检索到多个片段后，为什么还要放进 Prompt 模板？

因为 Prompt 可以明确告诉 LLM：`这些是检索到的上下文、哪些是用户问题、回答时要遵守什么规则`。

## 11. 为什么检索片段最好加编号或分隔符？

因为这样可以让 LLM 知道 `这是多个独立片段，不是一整段连续原文`

## 12.如果 Prompt 里写“只能根据检索内容回答”，是在约束什么？
是在约束 LLM `不要脱离资料凭空发挥，尽量基于检索到的内容回答`。

## 13. 什么叫“固定 RAG 流程”？
就是流程写死成 `先检索，再把结果交给 LLM 回答`，每次都按同一套步骤走。

## 14. 什么时候更适合固定 RAG，而不是 Agent + Tool？
当场景里 `每次都必须先查知识库再回答` 时，更适合固定 RAG，因为它更简单、更稳定、更好调试。

## 15. 什么时候更适合 Agent + Tool？
当流程不固定，或者有多个工具可选时，更适合 `Agent + Tool`，让 LLM 决定要不要查、查哪个、查几次。

## 16. Memory 在完整 RAG 流程里起什么作用？
`Memory` 负责记住多轮聊天上下文，让系统知道你前面问过什么、现在是不是在追问。

## 17. 为什么说 Memory 不能替代 Retriever？
因为 `Memory `记的是聊天记录，`Retriever `查的是外部知识库，它们职责不同。

## 18.如果 RAG 答得差，应该先查哪里？

先查 `检索有没有找对`，再查 `Prompt 和 LLM 有没有答对`。

## 19. 如果知识库里明明有答案，但系统总检索不到，问题通常可能出在哪？

通常可能出在 `切分不合理、向量化效果一般、向量库设置不对、Retriever 参数不合适`。

## 20. 一句话怎么概括 RAG 主线？

`先读、先切、先存；再问、再找、再答`。

# Day9-demo

## 1. `create_documents([knowledge])` 和 `split_documents(...)`有什么区别？

```
create_documents 适合处理 原始文本字符串
split_documents 适合处理 已经是 Document 列表的数据
```

## 2. `txt_search.py` 中 为什么不能直接把 `uploaded_files `扔给 `TextLoader`，而是要先写到临时目录里，再去加载？

```
TextLoader 更适合接收"磁盘上的真实文件路径"，而 uploaded_files 是 Streamlit 上传组件返回的"内存里的上传文件对象"。

Streamlit 负责收文件，TextLoader 负责读文件，临时目录负责把两者接起来。
```

## 3. vectordb 和 retriever 到底区别是什么？

```
vectordb：向量库实例本体，类似仓库
retriever：从向量库实例里包装出来的统一检索接口，类似取货窗口

示例：
vectordb = Chroma.from_documents(splits, embeddings)
retriever = vectordb.as_retriever()

仓库本体 vectordb 能做的事情更底层、更多，比如：
	1. 存向量
	2. 带 metadata 存储
	3. 建索引
	4. 直接做相似度搜索
	5. 有时还能持久化磁盘
而 retriever 更专注一件事：
	给我一个问题，我给你最相关的 Document。
	所以它更像一个标准化接口，方便 LangChain 其他组件统一接入。

```

## 4. from_documents 是什么？

```
示例：
	FAISS.from_documents(documents, embeddings)
	Chroma.from_documents(documents, embeddings)
区别只是底层库不同：
	1.FAISS.from_documents(...)
		创建的是 FAISS 向量库实例
	2.Chroma.from_documents(...)
		创建的是 Chroma 向量库实例
它们的共同意思都是：
拿一批 Document，配一个 embedding 模型，直接创建对应的向量库

from_documents 不是某一个库独有的业务逻辑，而是“用文档直接建库”的常见入口写法。
```

## 5. st.session_state["messages"] 和 memory 有什么区别？

```
st.session_state["messages"] 是给页面显示聊天记录用的。

memory = ConversationBufferMemory(...)更偏LLM 对话层，负责让模型理解前面聊过什么。
```

## 6. 为什么要把 retriever 再包装成 tool？

```
Retriever 是检索能力，Tool 是给 Agent 调用的工具形态。

所以这里把 retriever 包成 tool，就是为了：
	让 Agent 能把"查文档"当作一个可调用工具来使用
也就是说，后面不再是程序员手写死：先检索 -> 再回答
而是让 Agent + LLM 来决定：
	1. 要不要查文档
	2. 什么时候查
	3. 查完再怎么回答
把 retriever 包成 tool，是为了把检索能力交给 Agent 使用。
```

## 7. base_prompt_template 和前面的 instructions 有什么区别？

```
instructions 更像是 具体要求 管内容规则
	也就是“你是谁、你必须怎么回答、查不到怎么办”。
base_prompt_template 更像是：整体骨架 / 流程格式 管提示词结构
	也就是“工具怎么写、思考格式怎么写、历史消息放哪、用户输入放哪、最后答案放哪”。
```

## 8. 执行器和 agent 到底区别是什么？

```
agent 主要负责：思考和决策的核心逻辑
	1. 看 prompt
	2. 看用户问题
	3. 决定要不要用工具
	4. 决定调用哪个工具
	5. 组织下一步输出格式
agent_executor 是在 agent 外面再包一层，负责：
	1. 真正去执行 agent 决定的动作
	2. 调工具
	3. 把工具结果再喂回 agent
	4. 处理多轮 Thought/Action/Observation
	5. 接 memory
	6. 打日志 verbose=True
	7. 处理解析异常 handle_parsing_errors=True
```

## 9. open(…).read() 和 TextLoader.load() 有啥区别吗？

```
open(...).read() 读出来的是原始字符串
TextLoader.load() 读出来的是Document 列表
```

## 10. `tempfile.TemporaryDirectory(dir=r"D:\\")` 和普通的创建文件夹有什么不同？

`临时上传 -> TemporaryDirectory`
`长期存档 -> uploads 文件夹`

## 11. 为什么不能拿 st.session_state[“messages”] 当 memory？

```
session_state 负责前端显示，memory 负责模型上下文。

因为 st.session_state["messages"] 只是前端页面自己的聊天记录，它主要负责“显示”。
它并不是 LangChain 规定的 memory 接口，不会自动把历史整理好再塞进 prompt 给 LLM。
而 memory 的作用是：
 1. 按照 LangChain 的规则管理历史消息
 2. 知道历史变量名叫 {chat_history}
 3. 知道最终回答要从 output 里取
 4. 在 invoke() 前自动读历史
 5. 在 invoke() 后自动写回这一轮回答
```

## 12.`agent_executor.invoke(...)` 真正触发了什么？

```
这里真正触发的是一整套 Agent 流程：
读取 memory 里的历史记录
把历史填进 prompt 的 {chat_history}
把当前问题填进 {input}
让 Agent 思考要不要调用工具
如果要，就调用 tool，而 tool 背后才会去用 retriever
最后让 LLM 生成最终回答
返回 response
所以最准确的一句是：
invoke() 触发的是“Agent + Tool + Memory + LLM”的完整执行流程。
```

## 13. PyPADLoader 和 OCR 有什么区别？

```
能直接提取文字的 PDF：用 PyPDFLoader
提不出文字的 PDF：再走 OCR
OCR 的流程：
	1. PDF 每一页转成图片
	2. 对每张图片做 OCR
	3. 拿到识别出的文字
	4. 把文字包装成 Document(page_content=..., metadata=...)
```

## 14. ReAct 风格和固定 RAG 的区别

* 固定RAG**：流程是写死的**
* ReAct Agent**：流程让大模型自己决定

```
只要出现这套格式，基本就是在走 ReAct 风格：
    Thought: ...
    Action: ...
    Action Input: ...
    Observation: ...
    Final Answer: ...
```



# txt_search.py 流程

1. 用户在 `Streamlit` 页面上传 `txt `文件
2. 程序用 `TextLoader `读取文档，并用 `RecursiveCharacterTextSplitter `切分
3. 把切片做 `Embedding`，存入 `Chroma `向量库
4. 从向量库中创建统一检索接口 `retriever`
5. 再把 `retriever `包装成 `tool`，交给 `agent `使用
6. 同时准备 `memory `和页面聊天记录
7. 用户提问后，调用 `agent_executor`
8. `Agent` 视情况调用文档检索工具，最后生成回答并显示到页面上





















