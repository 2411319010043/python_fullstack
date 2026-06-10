import base64
import mimetypes
from pathlib import Path
from urllib.request import Request, urlopen

from config import create_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# what：定义图片理解工具的输入参数结构
# why：LangChain 需要知道这个工具调用时要传哪些参数
# how：image_source 接收本地路径或公网 URL，question 接收用户想问的问题
class ImageUnderstandingInput(BaseModel):
    image_source: str = Field(description="图片来源，可以是本地图片路径或公网图片 URL")
    question: str = Field(description="用户针对图片提出的问题")


# what：判断传入的图片来源是不是公网 URL
# why：本地图片和公网图片的处理方式不同
# how：如果字符串以 http:// 或 https:// 开头，就认为它是 URL
def is_url(image_source: str) -> bool:
    return image_source.startswith(("http://", "https://"))


# what：根据图片来源猜测 MIME 类型
# why：拼接 data URL 时需要告诉模型这是什么类型的图片
# how：优先用 mimetypes 根据路径或 URL 后缀推断，推断失败时默认使用 image/jpeg
def guess_mime_type(image_source: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_source)
    if mime_type and mime_type.startswith("image/"):
        return mime_type
    return "image/jpeg"


# what：把图片二进制内容转换成 data URL
# why：多模态模型接收图片时可以直接使用 data URL，而不是依赖外部地址
# how：先把图片二进制内容做 base64 编码，再按 data:image/...;base64,... 的格式拼接
def bytes_to_data_url(image_bytes: bytes, mime_type: str) -> str:
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{image_base64}"


# what：把本地图片转换成 data URL
# why：模型不能直接访问你电脑上的本地路径
# how：读取本地文件二进制内容，再调用 bytes_to_data_url 生成 data URL
def local_image_to_data_url(image_path: str) -> str:
    path = Path(image_path)
    image_bytes = path.read_bytes()
    mime_type = guess_mime_type(image_path)
    return bytes_to_data_url(image_bytes, mime_type)


# what：把公网图片转换成 data URL
# why：有些模型链路无法稳定下载外部图片，先由我们下载再传给模型更稳
# how：用 urllib 下载图片内容，拿到 content-type 后转成 data URL
def remote_image_to_data_url(image_url: str) -> str:
    request = Request(
        image_url,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urlopen(request, timeout=20) as response:
        image_bytes = response.read()
        mime_type = response.headers.get_content_type()

    if not mime_type or not mime_type.startswith("image/"):
        mime_type = guess_mime_type(image_url)

    return bytes_to_data_url(image_bytes, mime_type)


# what：统一把图片来源转换成模型可用的 data URL
# why：无论用户给的是本地路径还是公网 URL，后面都希望走同一种图片输入格式
# how：先判断是不是 URL，再分别调用本地或公网图片转换函数
def image_source_to_data_url(image_source: str) -> str:
    if is_url(image_source):
        return remote_image_to_data_url(image_source)
    return local_image_to_data_url(image_source)


# what：图片理解工具的核心函数
# why：真正完成图片分析和回答问题的逻辑都在这里
# how：先把图片转成 data URL，再把问题和图片一起发给多模态模型
def understand_image(image_source: str, question: str) -> str:
    image_url = image_source_to_data_url(image_source)

    message = HumanMessage(
        content=[
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
    )

    model = create_chat_model()
    response = model.invoke([message])
    return response.content


# what：把图片理解函数封装成 LangChain 工具
# why：封装后它才能被代码 invoke，也能被 Agent 当成工具来调用
# how：通过 StructuredTool.from_function 指定函数、名称、说明和参数结构
image_understanding_tool = StructuredTool.from_function(
    func=understand_image,
    name="image_understanding_tool",
    description="根据图片路径或图片 URL 分析图片内容，并结合用户问题返回中文回答。",
    args_schema=ImageUnderstandingInput,
)
