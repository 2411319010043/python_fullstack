# what：导入 asyncio，用来运行异步测试函数
# why：wiki_search_tool 使用 ainvoke 异步调用，需要事件循环执行
# how：用 asyncio.run(main()) 启动 async main
import asyncio
# what：导入项目中封装好的维基百科搜索 Tool
# why：测试文件只负责调用 Tool，不重复定义 Tool 逻辑
# how：从 tools.wikipedia_tool 导入 wiki_search_tool
from tools.wikipedia_tool import wiki_search_tool


# what：定义异步 main 函数，用于测试维基百科 Tool
# why：await 只能写在 async 函数内部
# how：调用 wiki_search_tool.ainvoke(...) 并打印结果
async def main():

    # what：异步调用维基百科搜索 Tool
    # why：验证 wiki_search_tool 是否能接收 query 并返回百科摘要
    # how：ainvoke 传入参数字典，query 要和 WikiSearchInput 字段名一致
    result = await wiki_search_tool.ainvoke({"query":"LangChain"})
    print(result)


# what：判断当前文件是否被直接运行
# why：直接运行 examples/run_wikipedia_tool.py 时才执行测试
# how：__name__ 等于 "__main__" 时，用 asyncio.run(main()) 启动异步函数
if __name__ == "__main__":
    asyncio.run(main())