# what：导入 FAISS、Embedding 和 PDF 加载器
# why：这个例子不只是读 pdf，还要做向量检索
# how：分别导入 FAISS、OpenAIEmbeddings、PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
# what：导入 HuggingFace embedding 封装器。
# why：FAISS 建立向量索引之前，必须先把文本转换成向量。
# how：使用 LangChain 的 HuggingFaceEmbeddings 调用本地模型。
from langchain_huggingface import HuggingFaceEmbeddings


import os

BASE_DIR = os.path.dirname(__file__)

# what：指定要读取的 pdf 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/pytorch.pdf")
)

loader = PyPDFLoader(file_path)
# what：加载并切分 pdf
# why：先把 pdf 读成适合向量检索的片段
# how：调用 PyPDFLoader(...).load_and_split()
pages = loader.load_and_split()
# what：实例化 embedding 模型。
# why：FAISS 建库前需要先把文本列表向量化。
# how：继续使用本地模型 all-MiniLM-L6-v2。
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# what：从文档创建 FAISS 向量库
# why：要先把文本向量化并建立索引，后面才能做相似度搜索
# how：调用 FAISS.from_documents(pages, OpenAIEmbeddings())
faiss_index = FAISS.from_documents(pages, embeddings)
# what：对问题做相似度检索
# why：演示如何从 pdf 中找出和问题最相关的内容
# how：调用 faiss_index.similarity_search("What is PyTorch?", k=2)
docs = faiss_index.similarity_search("What is PyTorch?", k=2)
# what：打印检索结果的页码和部分正文
# why：既要看检索到了什么，也要看它来自哪一页
# how：从 metadata 取 page，从 page_content 取前 300 个字符
for doc in docs:
    print(str(doc.metadata["page"]) + ":", doc.page_content[:300])
