# pip install --quiet langchain_experimental langchain_openai
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

# 这是一个长文档，我们可以将其拆分。
with open("../../resource/knowledge.txt", encoding="utf-8") as f:
    knowledge = f.read()

text_splitter = SemanticChunker(OpenAIEmbeddings())
# what：给语义切分器设置断点阈值规则
# why：我们想控制“语义变化多大时才切开”
# how：通过 breakpoint_threshold_type 和 breakpoint_threshold_amount 调整切分保守程度
text_splitter = SemanticChunker(
    OpenAIEmbeddings(), breakpoint_threshold_type="percentile", breakpoint_threshold_amount=90
)
# what：执行语义切分并观察块数量
# why：验证更高阈值下，切分会更保守、块通常更少更大
# how：调用 create_documents([knowledge])，再打印 docs 和 len(docs)
docs = text_splitter.create_documents([knowledge])
print(docs[0].page_content)
print(docs[1].page_content)
print(len(docs))

