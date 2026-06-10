# what：导入项目中创建好的综合 Agent
# why：run_agent.py 只负责演示调用，不重复创建 Agent
# how：从 agents.assistant_agent 导入 agent 后使用 agent.invoke(...) 调用
from agents.assistant_agent import agent
from parsers.output_parsers_demo import format_text_as_json

def infer_task_type(question: str) -> str:
    if "天气" in question or "温度" in question or "风速" in question:
        return "weather"
    if "图片" in question or ".jpg" in question or ".png" in question or ".jpeg" in question or "image" in question:
        return "image"
    if "搜索" in question or "最新" in question or "新闻" in question:
        return "search"
    if "谁是" in question or "是什么" in question or "百科" in question:
        return "wiki"
    return "chat"

# what：封装一次 Agent 问答调用
# why：多个测试问题都要执行相同的 invoke 和打印逻辑，封装函数可以减少重复
# how：传入 question，构造 messages 输入，打印 Agent 返回的最后一条消息
def ask_agent(question: str) -> None:
    # what：向 Agent 发送用户消息
    # why：新版 create_agent 使用 messages 列表作为输入
    # how：role="user" 表示用户消息，content 放用户问题
    task_type = infer_task_type(question)
    response = agent.invoke(
        {"messages":[
            {"role":"user","content":question}
            ]
        }
    )
    final_answer = response["messages"][-1].content
    structured = format_text_as_json(task_type, final_answer)
    print(question)
    print(final_answer)
    print(structured)
    print("-" * 50)



# what：直接运行本文件时执行综合 Agent 演示
# why：集中测试普通聊天、天气查询、网页搜索和图片理解能力
# how：依次调用 ask_agent(...) 发送不同类型的问题
if __name__ == "__main__":
    ask_agent("你好，介绍一下你自己")
    ask_agent("今天北京天气怎么样？")
    ask_agent("帮我搜索一下 LangChain 最新版本更新了什么")
    ask_agent(
        r"请分析这张图片：D:\yl-workplace\github_code\python_fullstack\聚客\day7\day7-demo\day7-demo\images\scene1.jpg，这张图片里有什么？请用中文描述。"
    )