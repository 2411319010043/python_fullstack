# what：BaseModel 和 Field 用来定义 JSON 输出结构
# why：JsonOutputParser 需要知道模型应该输出哪些字段、字段类型和含义
# how：继承 BaseModel，并用 Field(description=...)描述字段
from pydantic import BaseModel, Field
# what：用来约束并解析成 JSON、XML 输出
# why：让模型按指定 JSON、XML 字段输出
# how：JsonOutputParser(pydantic_object=某个 BaseModel)、XMLOutputParser(tags=[...])
from langchain_core.output_parsers import JsonOutputParser, XMLOutputParser
# what：PromptTemplate 用来创建提示词模板
# why：我们需要把用户问题和 parser 生成的格式要求组合成完整提示词
# how：在 template 中写 {query} 和 {format_instructions} 这类占位符
from langchain_core.prompts import PromptTemplate
# what：从项目配置文件中导入统一的模型创建函数
# why：避免每个文件重复写 ChatOpenAI(...) 和环境变量读取逻辑
# how：项目根目录下有 config.py，运行时从项目根目录启动即可导入
from config import create_chat_model


# what：定义统一结构化响应的 JSON 输出模型
# why：不同来源的文本结果可以统一整理成相同字段，方便后续程序处理
# how：用 task_type、summary、key_points 描述任务类型、摘要、关键点
class UnifiedResponse(BaseModel):
    task_type: str = Field(description="任务类型，例如 weather、image、wiki、search、chat")
    summary: str = Field(description="对原始内容的一句话总结")
    key_points: list[str] = Field(description="从原始内容中提取的关键点列表")

# what：创建项目统一使用的聊天模型
# why：Output Parser 只负责约束和解析，真正生成结构化内容的是大模型
# how：通过 create_chat_model() 复用 config.py 中的模型配置
model = create_chat_model()

# what：创建 JSON 输出解析器
# why：让模型按照 UnifiedResponse 的字段输出 JSON
# how：把 UnifiedResponse 传给 JsonOutputParser 的 pydantic_object 参数
json_parser = JsonOutputParser(pydantic_object=UnifiedResponse)

# what：创建 XML 输出解析器
# why：让模型按照指定标签生成 XML
# how：通过 tags 指定期望使用的 XML 标签
xml_parser = XMLOutputParser(tags=["response", "task_type", "summary", "key_points", "point"])


json_prompt = PromptTemplate(
    template="""请把下面的原始文本整理成统一结构化响应。
任务类型：{task_type}
原始文本：{text}
{format_instructions}""",
# what：input_variables 表示这个 PromptTemplate 在调用时需要外部传入哪些变量。
# why：task_type 是任务类型、text 是原始文本
# how：后面调用 json_chain.invoke(...) 时，需要传入 task_type 和 text，LangChain 会把它们替换到模板中的对应占位符。
input_variables=["task_type", "text"],
# what：partial_variables 表示提前固定好的模板变量。
# why：format_instructions 不是用户每次输入的内容，而是 parser 自动生成的格式要求。每次都一样，所以可以提前放进去
# how：用 json_parser.get_format_instructions() 生成格式说明，并绑定到模板里的 {format_instructions}
partial_variables={"format_instructions":json_parser.get_format_instructions()}
)

# what：创建 XML 格式化提示词模板
# why：需要告诉模型把原始文本整理成统一 XML 结构
# how：运行时传入 task_type 和 text，并提前注入 xml_parser 的格式说明
xml_prompt = PromptTemplate(
    template="""请把下面的原始文本整理成统一结构化响应。
任务类型：{task_type}
原始文本：{text}
{format_instructions}""",
input_variables=["task_type", "text"],
partial_variables={"format_instructions":xml_parser.get_format_instructions()}
)

# what：创建 JSON 输出链
# why：把提示词、模型和 JSON 解析器串起来形成完整流程
# how：使用 LCEL 的 | 操作符按 prompt -> model -> parser 的顺序连接
json_chain = json_prompt | model | json_parser
# what：创建 XML 输出链
# why：把提示词、模型和 XML 解析器串起来形成完整流程
# how：使用 LCEL 的 | 操作符按 prompt -> model -> parser 的顺序连接
xml_chain = xml_prompt | model | xml_parser

# what：创建 JSON 调用链函数
# why：对外暴露清晰能力
# how：传入 task_type、text，调用链，返回结果
def format_text_as_json(task_type: str, text: str) -> dict:
    response = json_chain.invoke({
        "task_type":task_type,"text":text
    })
    return response

# what：创建 XML 调用链函数
# why：对外暴露清晰能力
# how：传入 task_type、text，调用 xml_chain，返回结果
def format_text_as_xml(task_type: str, text: str):
    response = xml_chain.invoke({
        "task_type":task_type,"text":text
    })
    return response
