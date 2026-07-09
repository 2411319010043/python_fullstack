# what：导入语义切分器和 Embedding
# why：语义切分不是主要看符号，而是要根据语义变化来判断哪里该断开
# how：导入 SemanticChunker 和 OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

# 这是一个长文档，我们可以将其拆分。
with open("../../resource/knowledge.txt", encoding="utf-8") as f:
    knowledge = f.read()
# what：创建语义切分器
# why：要先有 embedding 能力，才能比较相邻文本的语义变化
# how：把 OpenAIEmbeddings() 传给 SemanticChunker
text_splitter = SemanticChunker(OpenAIEmbeddings())

#拆分的默认方式是基于百分位数。在此方法中，计算所有句子之间的差异，然后任何大于50%的差异都会被拆分。
text_splitter = SemanticChunker(
    OpenAIEmbeddings(), breakpoint_threshold_type="percentile"
)
# what：把长文本按语义切块
# why：希望切出来的是“意思更完整”的块，而不只是长度差不多的块
# how：调用 text_splitter.create_documents([knowledge])
docs = text_splitter.create_documents([knowledge])
print(docs[0].page_content)
