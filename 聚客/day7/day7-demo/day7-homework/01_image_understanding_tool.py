# what：导入 base64 模块，用来处理二进制数据编码
# why：多模态模型不能访问本地路径，需要把图片内容打包进请求
# how：读取图片 bytes 后，用 base64.b64encode(image_bytes).decode("utf-8") 编码
import base64
# what：导入 os，用来读取 .env 中的环境变量
# why：base_url 和 api_key 不应该写死在代码里，方便切换环境
# how：用 os.getenv("变量名") 读取 .env 中配置的值
import os
# what：load_dotenv 用来读取 .env 文件中的环境变量
# why：API key 不应该写死在代码里，放在 .env 中更安全，也方便更换
# how：调用 load_dotenv() 后，ChatOpenAI 可以从环境变量中读取 OPENAI_API_KEY
from dotenv import load_dotenv
# what：导入 Path，用于处理本地文件路径
# why：Path 比普通字符串路径更适合读取文件、判断文件是否存在
# how： Path(image_path).read_bytes() 可以读取图片二进制内容
from pathlib import Path

# what：BaseModel 和 Field 用来定义 Tool 的参数结构
# why：LangChain 需要清楚知道 Tool 有哪些参数、类型和说明
# how： 继承 BaseModel，并用 Field(description=...) 描述每个参数
from pydantic import BaseModel, Field
# what：HumanMessage 是 LangChain 中表示“用户消息”的消息对象
# why：多模态输入需要把文本和图片一起包装成一条用户消息发给模型
# how：用 HumanMessage(content[{文本块}，{图片块}]) 构造多模态消息
from langchain_core.messages import HumanMessage
# what：StructuredTool 用来把普通 Python 函数封装成 LangChain Tool
# why：封装后函数才有 name、description、args_schema，方便模型或代码调用
# how：用 StructuredTool.from_function(...) 指定函数、工具名、说明和参数模型
from langchain_core.tools import StructuredTool
# what：ChatOpenAI 是 LangChain 中调用 OpenAI 聊天模型的类
# why：图片理解需要调用支持视觉能力的多模态模型，例如 gpt-4o
# how：用 ChatOpenAI(model="gpt-4o") 创建模型，再调用 model.invoke([message])
from langchain_openai import ChatOpenAI

# what：load_dotenv() 用来读取 .env 文件中的配置
# why：API key、base_url 这类敏感或易变配置不适合写死在代码里
# how：调用后，可以通过 os.getenv("变量名") 读取 .env 中的值
load_dotenv()


# what：ImageUnderstandingInput 定义图片理解 Tool 的输入参数结构
# why：Tool 需要明确告诉 LangChain 和大模型调用时要传哪些参数
# how：image_source 接收图片路径或 URL，question 接收用户针对图片的问题
class ImageUnderstandingInput(BaseModel):
    image_source: str = Field(description="图片来源，可以是公网URL，也可以是本地路径")
    question: str = Field(description="用户针对图片提出的问题")


# what：is_url 用来判断图片来源是否是网络 URL
# why：公网 URL 可以直接传给模型，本地路径需要先转成 base64 data URL
# how：检查 image_source 是否以 http:// 或 https:// 开头
def is_url(image_source: str) -> bool:
    if image_source.startswith(("http://","https://")):
        return True
    return False


# what：local_image_to_data_url 是一个把本地图片路径转换成 data URL 的函数
# why：多模态模型不能访问用户电脑上的本地路径，需要把图片内容编码后直接放进请求
# how：传入本地图片路径字符串，返回 data:image/jpeg;base64,... 格式的字符串
def local_image_to_data_url(image_path: str) -> str:

    # what：把字符串形式的图片路径转换成 Path 对象
    # why：Path 对象提供 read_bytes() 等文件读取方法，比直接操作字符串更方便
    # how：Path(image_path) 会根据传入的路径创建一个文件路径对象
    path = Path(image_path)

    # what：读取本地图片文件的二进制内容
    # why：图片不是普通文本，必须按 bytes 读取，才能正确进行 base64 编码
    # how：read_bytes() 会返回图片文件的原始二进制数据
    image_bytes = path.read_bytes()

    # what：把图片二进制内容编码成 base64 字符串
    # why：模型请求里不能直接放二进制 bytes，需要转成可传输的文本字符串
    # how：base64.b64encode(image_bytes) 得到 bytes，再 decode("utf-8") 转成 str
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # what：把 base64 图片内容拼成标准 data URL
    # why：多模态消息的 image_url.url 需要能识别图片类型和编码方式
    # how：data:image/jpeg;base64, 前缀说明这是 JPEG 图片，后面跟图片的 base64 内容
    return f"data:image/jpeg;base64,{image_base64}"


# what：understand_image 是图片理解 Tool 的核心函数
# why：Tool 本身不理解图片，需要在函数内部处理图片来源并调用视觉大模型
# how：接收 image_source 和 question，返回模型对图片问题的回答文本
def understand_image(image_source: str, question: str) -> str:

    # what：根据 image_source 判断图片是否来自公网 URL
    # why：公网 URL 可以直接传给模型，本地路径需要先转成 base64 data URL
    # how：如果不是 URL，就调用 local_image_to_data_url；否则直接使用原始 URL
    if not is_url(image_source):
        image_url = local_image_to_data_url(image_path=image_source)
    else:
        image_url = image_source

    # what：构造一条包含文本和图片的用户消息
    # why：多模态模型需要同时接收用户问题和图片内容，才能针对图片回答问题
    # how：content 列表中第一个块放文本问题，第二个块放图片 URL 或 data URL
    message = HumanMessage(
        content=[
            {"type":"text","text":question},
            {"type":"image_url","image_url":{"url":image_url}}
        ]
    )

    # what：创建通过中转服务调用的聊天/视觉模型
    # why：你的模型请求不是直接发到 OpenAI 官方地址，而是发到本地中转地址
    # how：api_key 和 base_url 从 .env 读取，model 写中转服务支持的模型名
    model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0,
    )

    # what：把多模态消息发送给模型并获取响应
    # why：真正理解图片和生成回答的是视觉大模型
    # how：聊天模型接收消息列表，所以即使只有一条 message，也要写成 [message]
    response = model.invoke([
        message
    ])

    # what：返回模型回答的正文内容
    # why：Tool 调用者需要拿到图片分析结果，而不是只在控制台打印
    # how：response.content 是 AIMessage 中的文本回答
    return response.content


# what：把 understand_image 普通函数封装成 LangChain Tool
# why：封装后工具才有名称、说明和参数结构，方便手动 invoke 或交给 Agent 调用
# how：用 StructuredTool.from_function 指定核心函数、工具名、工具说明和参数模型
image_understanding_tool = StructuredTool.from_function(

    # what：指定这个 Tool 真正执行时要调用的 Python 函数。
    # why：Tool 本身只是包装壳，真正干活的是 understand_image。
    # how：当 image_understanding_tool.invoke(...) 被调用时，内部会执行 understand_image(...)。
    func=understand_image,

    # what：指定工具名称。
    # why：大模型或 Agent 需要通过工具名识别和选择工具。
    # how：如果 Agent 决定调用这个工具，会生成类似 name="image_understanding_tool" 的工具调用。
    name="image_understanding_tool",

    # what：指定工具说明。
    # why：这是给大模型看的说明书，帮助模型判断什么时候应该调用这个工具。
    # how：要写清楚工具能做什么、适合什么场景、返回什么结果。
    description="根据图片来源和用户问题分析图片内容，并返回中文回答。适合回答图片中有什么、场景、物体、天气等问题。",

    # what：指定工具的参数结构。
    # why：LangChain 和大模型需要知道调用这个工具时应该传哪些参数。
    # how：ImageUnderstandingInput 里定义了 image_source 和 question 两个字段。
    args_schema=ImageUnderstandingInput
)

# what：测试入口，用于直接运行当前文件时测试图片理解 Tool
# why：作业文件既可以被直接运行测试，也可以被其他文件导入复用
# how：只有当当前文件作为主程序运行时，__name__ 才等于 "__main__"
if __name__ == "__main__":

    # what：调用 image_understanding_tool 执行一次图片理解测试
    # why：验证 Tool 是否能接收图片来源和问题，并返回模型分析结果
    # how：invoke 传入字典，key 要和 ImageUnderstandingInput 中的字段名一致
    result = image_understanding_tool.invoke(
        {
            "image_source":r"D:\yl-workplace\github_code\python_fullstack\聚客\day7\day7-demo\day7-demo\images\scene1.jpg",
            "question":"这张图片里有什么？请用中文描述。",
        }
    )

    print(result)