# what：导入新版 Tavily 搜索 Tool
# why：TavilySearchResults 已被标记为 deprecated，新项目中推荐使用 langchain-tavily 包
# how：安装 langchain-tavily 后，从 langchain_tavily 导入 TavilySearch
from langchain_tavily import TavilySearch

# what：创建网页搜索 Tool
# why：Agent 遇到最新信息、网页资料、新闻类问题时，需要调用搜索工具
# how：max_results=1 表示最多返回 1 条搜索结果，TAVILY_API_KEY 会从环境变量中读取
search_tool = TavilySearch(max_results=1)

