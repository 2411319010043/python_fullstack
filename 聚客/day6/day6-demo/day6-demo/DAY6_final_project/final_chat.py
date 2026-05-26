import os 

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda

from DAY6_final_project.few_shot.selector_few_shot import few_shot_prompt,llm
from DAY6_final_project.cache.chat_cache import get_cache,set_cache
from DAY6_final_project.chat_history.history_chat import get_session_history

final_prompt = ChatPromptTemplate.from_messages([
    ("system","你是一名面向初学者的 Python 和 LangChain 编程助教。这里的 LangServe 专指 LangChain 生态中的 LangServe。回答必须严格按照“定义：”“作用：”“例子：”三行输出。语言要通俗易懂，不要输出无关内容，不要猜测其他术语，不要输出多余引号、乱码或重复标点。"),
    few_shot_prompt,
    MessagesPlaceholder("history"),
    ("human","{question}")
])

base_chain = final_prompt | llm

chain_with_history = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

def chat_with_cache(input_data, config):
    question = input_data["question"]
    session_id = config["configurable"]["session_id"]
    cached = get_cache(session_id,question)
    # 先查缓存
    if cached is not None:
        answer = cached["answer"]
        history = get_session_history(session_id)
        # 手动添加聊天历史记录
        history.add_messages(
            [
                HumanMessage(content=question),
                AIMessage(content=answer)
            ]
        )
        return {
            "answer":answer,
            "usage":{
                "input_tokens":0,
                "output_tokens":0,
                "total_tokens":0,
            },
            "from_cache":True,
        }
    
    # 未命中缓存走大模型
    response = chain_with_history.invoke(
        {"question":question},
        config={"configurable":{"session_id":session_id}}
    )
    answer = response.content
    usage = response.usage_metadata or {}
    # 添加缓存
    set_cache(session_id=session_id, question=question, data={"answer":answer, "usage":usage, "from_cache":False})
    return {
        "answer":answer,
        "usage":usage,
        "from_cache":False
    }

final_chain = RunnableLambda(chat_with_cache)


if __name__ == "__main__":
    final_answer1 = final_chain.invoke(
        {"question":"什么是 LangChain?"},
        config={"configurable":{"session_id":"u2"}}
    )
    print(final_answer1)
    final_answer2 = final_chain.invoke(
        {"question":"什么是 LangChain?"},
        config={"configurable":{"session_id":"u2"}}
    )  
    print(final_answer2)
