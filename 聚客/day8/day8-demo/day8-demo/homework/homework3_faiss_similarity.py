# what：导入 HuggingFace embedding 封装器。
# why：FAISS 建立向量索引之前，必须先把文本转换成向量。
# how：使用 LangChain 的 HuggingFaceEmbeddings 调用本地模型。
from langchain_huggingface import HuggingFaceEmbeddings

# what：导入 FAISS 向量检索工具。
# why：作业 3 的目标就是实现一个基于 FAISS 的 Similarity Search 例子。
# how：使用 langchain_community.vectorstores 中的 FAISS。
from langchain_community.vectorstores import FAISS

# what：准备短句知识列表。
# why：这道题只需要一个最小相似度搜索示例，短句列表就足够展示核心流程。
# how：每条文本本身就是独立检索单元，所以这里不需要额外切分。
documents = [
    "Pixar 是一家动画工作室。",
    "苹果公司开发 iPhone。",
    "Python 是一门编程语言。",
    "人工智能正在改变世界。",
]

# what：实例化 embedding 模型。
# why：FAISS 建库前需要先把文本列表向量化。
# how：继续使用本地模型 all-MiniLM-L6-v2。
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# what：使用文本列表创建 FAISS 向量库。
# why：documents 现在是字符串列表，不是 Document 对象列表，所以更适合 from_texts。
# how：把 documents 和 embeddings 传给 FAISS.from_texts。
vector = FAISS.from_texts(documents, embeddings)


# what：程序入口。
# why：只在直接运行当前脚本时执行测试查询。
# how：使用 __name__ == "__main__"。
if __name__ == "__main__":
    # what：准备测试问题。
    # why：用一个和 Pixar 相关的 query 验证 FAISS 的相似度检索效果。
    # how：把 query 设置为“Pixar是什么？”。
    query = "Pixar是什么？"

    # what：执行带分数的 FAISS 检索。
    # why：不仅要看最相似文本是什么，还想顺便看检索分数。
    # how：调用 vector.similarity_search_with_score(query=query, k=1)。
    docs_and_scores = vector.similarity_search_with_score(query=query, k=1)

    # what：打印检索结果和分数。
    # why：最小示例里直接把返回值整体打出来，方便观察返回结构。
    # how：输出 docs_and_scores 这个由 (Document, score) 组成的列表。
    print(docs_and_scores)
