import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个编程助教。"),
    ("human","{question}")]
)

llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    temperature=0
)

chain = prompt | llm

if __name__ == "__main__":
    question = input("请输入你的问题：")
    response = chain.invoke({"question":question})
    print(response.usage_metadata)
    print("-----------------------------------")
    print(response.response_metadata)