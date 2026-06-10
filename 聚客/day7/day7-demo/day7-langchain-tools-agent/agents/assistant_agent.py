# 创建一个可以聊天、查天气、搜网页、理解图片、查询百科的综合 Agent。

# what：导入 LangChain Agent 创建函数
# why：当前项目需要创建一个能根据用户问题自动调用工具的 Agent
# how：create_agent(model=..., tools=..., system_prompt=...) 返回可调用的 Agent
from langchain.agents import create_agent
# what：导入项目统一的模型创建函数
# why：Agent 需要聊天模型来理解用户问题、决定是否调用工具并生成最终回答
# how：调用 create_chat_model() 返回配置好的 ChatOpenAI 模型对象
from config import create_chat_model
# what：导入天气查询 Tool
# why：Agent 需要在用户询问天气时调用这个工具
# how：get_weather 已经被 @tool 封装，可以直接放进 tools 列表
from tools.weather_tool import get_weather
# what：导入网页搜索 Tool
# why：Agent 需要在用户询问最新信息或网页资料时调用这个工具
# how：search_tool 是 Tavily 搜索 Tool，可以直接放进 tools 列表
from tools.search_tool import search_tool
# what：导入图片理解 Tool
# why：综合 Agent 需要在用户提供图片路径或 URL 时分析图片内容
# how：image_understanding_tool 已经用 StructuredTool 封装，可以直接放进 tools 列表
from tools.image_tool import image_understanding_tool
# what：导入异步维基百科搜索 Tool
# why：综合 Agent 需要在用户询问百科概念、人物、地点、历史事件时查询百科摘要
# how：wiki_search_tool 已经用 StructuredTool 封装，可以放进 tools 列表供 Agent 调用
from tools.wikipedia_tool import wiki_search_tool


# what：创建综合 Agent 可用的工具列表
# why：Agent 需要知道自己有哪些外部工具可以调用
# how：把天气、网页搜索、图片理解和维基百科 Tool 放进同一个列表中
tools = [get_weather, search_tool,image_understanding_tool,wiki_search_tool]

# what：创建综合 LangChain Agent
# why：让模型可以根据用户问题自动决定直接回答，或调用天气、搜索、图片、百科工具
# how：传入模型对象、工具列表和系统提示词
agent = create_agent(
    model=create_chat_model(),
    tools=tools,
    system_prompt="""你是一个智能助手。
普通聊天直接回答。
当用户询问当前天气、温度、风速时，调用 get_weather 工具。
当用户询问最新信息、网页资料、新闻、搜索类问题时，调用网页搜索工具。
当用户提供图片路径或图片 URL，并询问图片内容时，调用 image_understanding_tool。
当用户询问百科概念、人物、地点、历史事件等稳定知识时，调用 async_wikipedia_search。
回答时使用中文。"""
)

