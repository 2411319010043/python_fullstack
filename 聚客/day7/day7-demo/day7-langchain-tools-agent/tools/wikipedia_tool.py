# 自定义维基百科搜索 Tool + 异步调用 ainvoke


# what：定义 Tool 输入参数结构
# why：让 LangChain 知道 Tool 需要 query 参数
# how：继承 BaseModel，用 Field 描述 query
from pydantic import BaseModel, Field
# what：封装普通函数或异步函数为 LangChain Tool
# why：Tool 才能支持 invoke / ainvoke
# how：用 StructuredTool.from_function(..., coroutine=异步函数)
from langchain_core.tools import StructuredTool
# what：LangChain 提供的维基百科查询封装
# why：真正查询百科内容的能力来自它
# how：创建 wrapper 后调用 wrapper.run(query)
from langchain_community.utilities import WikipediaAPIWrapper



# what：WikiSearchInput 定义维基百科搜索 Tool 的输入参数结构。
# why：LangChain 和大模型需要知道调用这个 Tool 时要传什么参数。
# how：query 接收要搜索的关键词、概念、人物、地点或问题。继承 BaseModel，每个字段用 Field(description=...) 说明含义
class WikiSearchInput(BaseModel):
    query: str = Field(description="要在维基百科中搜索的关键词或问题")


# what：异步维基百科搜索函数
# why：作业要求支持 ainvoke，所以核心函数写成 async def
# how：内部用 WikipediaAPIWrapper.run(query) 查询维基百科并返回结果
async def async_wikipedia_search(query: str) -> str:

    try:
        # what：创建维基百科 API 包装器
        # why：真正查询维基百科的能力来自 WikipediaAPIWrapper，而不是函数自己凭空知道
        # how：top_k_results=1 表示只取最相关的一条结果，doc_content_chars_max 表示最多返回 500 个字符
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)

        # what：使用 query 去维基百科搜索内容
        # why：用户传入的 query 是搜索关键词或问题，需要交给 api_wrapper 执行查询
        # how：api_wrapper.run(query) 会返回维基百科摘要文本
        result = api_wrapper.run(query)

        return result
    
    except Exception as error:
        # what：捕获维基百科查询过程中的异常
        # why：外部 API 可能网络失败、返回非 JSON 或被拦截，不能让整个程序崩溃
        # how：把异常转换成字符串结果返回给调用者
        return f"维基百科查询失败：{error}"


# what：同步维基百科搜索函数
# why：综合 Agent 使用 agent.invoke(...) 同步运行时，需要 Tool 支持同步调用
# how：内部调用 WikipediaAPIWrapper.run(query)，返回维基百科摘要文本
def wikipedia_search(query: str) -> str:
    try:
        api_wrapper = WikipediaAPIWrapper(
            top_k_results=1,
            doc_content_chars_max=500,
            lang="en",
        )
        return api_wrapper.run(query)
    except Exception as error:
        return f"维基百科查询失败：{error}"

# what：把异步维基百科搜索函数封装成 LangChain Tool
# why：封装后才能通过 ainvoke 进行异步调用，也方便未来交给 Agent 使用
# how：用 StructuredTool.from_function，并通过 coroutine 指定异步函数
wiki_search_tool = StructuredTool.from_function(

    # what：指定工具名称
    # why：LangChain 和未来的 Agent 需要通过工具名识别这个工具
    # how：传入字符串名称，表示这个工具叫 async_wikipedia_search
    name="async_wikipedia_search",

    # what：指定工具说明
    # why：说明这个工具能做什么；未来交给 Agent 时，大模型会根据它判断是否调用
    # how：用自然语言描述工具用途、适用场景和返回内容
    description='根据关键词异步搜索维基百科，并返回百科摘要',

    # what：指定工具输入参数结构
    # why：LangChain 需要知道调用工具时要传哪些参数，以及参数类型和含义
    # how：WikiSearchInput 中定义了 query 字段，表示维基百科搜索关键词或问题
    args_schema=WikiSearchInput,

    # what：指定工具的异步执行函数
    # why：作业要求支持异步调用，ainvoke 时需要执行这个 coroutine
    # how：传入 async_wikipedia_search 函数对象，不加引号
    coroutine=async_wikipedia_search,
    func=wikipedia_search,
)



