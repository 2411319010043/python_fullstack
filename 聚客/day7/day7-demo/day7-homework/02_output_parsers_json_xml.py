# 用 LangChain + Output Parser 实现 JSON 和 XML 格式输出。

# what：导入 os，用来读取环境变量
# why：API key 和中转地址放在 .env 中，不应该写死在代码里
# how：用 os.getenv("变量名") 获取 .env 中的配置
import os

# what：load_dotenv 用来加载 .env 文件
# why：让 Python 程序能读取 OPENAI_API_KEY 和 OPENAI_BASE_URL
# how：调用 load_dotenv(dotenv_path=env_path, override=True) 加载指定 .env
from dotenv import load_dotenv
# what：BaseModel 和 Field 用来定义 JSON 输出结构
# why：JsonOutputParser 需要知道模型应该输出哪些字段、字段类型和含义
# how：继承 BaseModel，并用 Field(description=...)描述字段
from pydantic import BaseModel, Field
# what：PromptTemplate 用来创建提示词模板
# why：我们需要把用户问题和 parser 生成的格式要求组合成完整提示词
# how：在 template 中写 {query} 和 {format_instructions} 这类占位符
from langchain_core.prompts import PromptTemplate
# what：JsonOutputParser 用来约束并解析 JSON 输出
# why：让模型按指定 JSON 字段输出，并把 JSON字符串解析成 Python dict
# how：JsonOutputParser(pydantic_object=某个 BaseModel)
from langchain_core.output_parsers import JsonOutputParser
# what：XMLOutputParser 用来约束并解析 XML 输出
# why：让模型按指定 XML 标签输出，并把 XML 结果
# how：XMLOutputParser(tags=[...]) 指定期望使用的 XML 标签
from langchain_core.output_parsers import XMLOutputParser
# what：ChatOpenAI 是 LangChain 中调用聊天模型的类
# why：需要调用大模型生成符合 JSON 或 XML 格式的内容
# how：指定 model、api_key、base_url 和 temperature 创建模型对象
from langchain_openai import ChatOpenAI

# what：load_dotenv() 用来读取 .env 文件中的配置
# why：API key、base_url 这类敏感或易变配置不适合写死在代码里
# how：调用后，可以通过 os.getenv("变量名") 读取 .env 中的值
load_dotenv()

# what：创建通过中转服务调用的聊天/视觉模型
# why：你的模型请求不是直接发到 OpenAI 官方地址，而是发到本地中转地址
# how：api_key 和 base_url 从 .env 读取，model 写中转服务支持的模型名
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0,
)


# what：定义模型最终要输出的 JSON 结构
# why：JsonOutputParser 需要根据它生成格式要求
# how：继承 BaseModel，每个字段用 Field(description=...) 说明含义
class WeatherReport(BaseModel):
    city: str = Field(description="城市名称")
    weather: str = Field(description="天气状况")
    max_temperature: str = Field(description="最高温度")
    min_temperature: str = Field(description="最低温度")

# what：创建 JSON 输出解析器
# why：让模型按照 WeatherReport 的字段结构输出 JSON
# how：把 WeatherReport 传给 JsonOutputParser 的 pydantic_object 参数
json_parser = JsonOutputParser(pydantic_object=WeatherReport)

json_prompt = PromptTemplate(
    # what：template 是提示词模板
    # why：我们需要把固定要求、格式说明、用户问题组合成一段完整 prompt 发给模型
    # how：在模板中写普通文本和占位符。普通文本会原样保留。{format_instructions} 和 {query} 会在运行时被替换成具体内容
    template="回答用户的问题，并严格按照格式要求输出。\n{format_instructions}\n{query}",
    # what：input_variables 表示这个 PromptTemplate 在调用时需要外部传入哪些变量。
    # why：query 是用户每次不同的问题，不能提前固定。
    # how：后面调用 chain.invoke({"query":"生成上海天气报告"}) 时， LangChain 会把 query 替换到模板里的 {query}
    input_variables=["query"],
    # what：partial_variables 表示提前固定好的模板变量。
    # why：format_instructions 不是用户每次输入的内容，而是 parser 自动生成的格式要求。她每次都一样，所以可以提前放进去。
    # how：用 json_parser.get_format_instructions() 生成格式说明，并绑定到模板里的 {format_instructions}
    partial_variables={"format_instructions":json_parser.get_format_instructions()}
)

# what：创建 JSON 输出链
# why：把提示词、模型和解析器串起来形成完整流程
# how：使用 LCEL 的 | 操作符 prompt -> model -> parser 的顺序连接
json_chain = json_prompt | model | json_parser



# what：创建 XML 输出解析器
# why：让模型按照指定标签生成 XML
# how：通过 tags 指定期望使用的 XML 标签
xml_parser = XMLOutputParser(tags=['weather_report','city','weather','max_temperature','min_temperature'])

xml_prompt = PromptTemplate(
    template="回答用户的问题，并严格按照 XML 格式要求输出。\n{format_instructions}\n{query}",
    input_variables=['query'],
    partial_variables={"format_instructions":xml_parser.get_format_instructions()}
)

# what：创建 XML 输出链
# why：把提示词、模型和 XML 解析器串起来形成完整流程
# how：使用 LCEL 的 | 操作符按 prompt -> model -> parser 的顺序连接
xml_chain = xml_prompt | model | xml_parser

# what：直接运行文件时测试 JSON 和 XML 输出链
# why：验证 JsonOutputParser 和 XMLOutputParser 是否都能正常解析模型输出
# how：分别调用 json_chain.invoke(...) 和 xml_chain.invoke(...)，并打印结果
if __name__ == "__main__":
    response_json = json_chain.invoke(
        {"query":"假设北京今天晴，最高温度 30°C，最低温度 20°C，请生成一个天气报告。"}
    )

    print(f"response_json:{response_json}")

    response_xml = xml_chain.invoke(
        {"query":"假设北京今天晴，最高温度 30°C，最低温度 20°C，请生成一个天气报告。"}
    )
    print(f"response_xml:{response_xml}")
