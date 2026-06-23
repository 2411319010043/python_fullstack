# what：导入 Path。
# why：相对路径在不同终端工作目录下容易出错，用脚本自身位置拼路径更稳。
# how：通过 pathlib.Path 获取当前脚本所在目录，再拼出 knowledge.txt 的绝对路径。
from pathlib import Path

# what：导入 Chroma。
# why：作业 2 的核心就是用 Chroma 实现本地向量库存储和查询。
# how：使用 langchain_chroma 包里的 Chroma 类。
from langchain_chroma import Chroma

# what：导入 HuggingFace embedding 封装器。
# why：这次本地向量库仍然需要先把文本切片转成向量。
# how：继续使用 all-MiniLM-L6-v2 本地模型。
from langchain_huggingface import HuggingFaceEmbeddings

# what：导入文本加载器。
# why：knowledge.txt 在磁盘上，需要先读进内存才能切分和建库。
# how：使用 TextLoader 读取 txt 文件。
from langchain_community.document_loaders import TextLoader

# what：导入字符级切分器。
# why：knowledge.txt 是长文本，不能整篇直接拿去做检索。
# how：使用 CharacterTextSplitter 把长文档切成更小片段。
from langchain_text_splitters import CharacterTextSplitter

# what：获取当前脚本所在目录。
# why：后面要基于脚本位置拼出 resource/knowledge.txt 的稳定路径。
# how：使用 Path(__file__).resolve().parent。
base_dir = Path(__file__).resolve().parent

# what：拼出 knowledge.txt 的实际路径。
# why：避免因为终端当前工作目录不同而找不到知识库文件。
# how：从当前脚本目录回到上一级，再进入 resource/knowledge.txt。
knowledge_path = base_dir.parent / "resource" / "knowledge.txt"

# what：创建文本加载器。
# why：告诉程序要读取哪份知识库文件，以及用什么编码读取中文。
# how：把 knowledge_path 转成字符串传给 TextLoader。
loader = TextLoader(str(knowledge_path), encoding="UTF-8")

# what：真正把 knowledge.txt 读进内存。
# why：只有 load() 之后，知识库内容才会变成 LangChain 可处理的 Document 列表。
# how：调用 loader.load() 返回原始 docs。
docs = loader.load()

# what：创建文本切分器。
# why：长文档整体向量化粒度太粗，不利于后续精准检索。
# how：把每块大小控制在 1500 个字符，并且不做块间重叠。
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)

# what：把原始文档切成多个小片段。
# why：后面要对“小块”而不是整篇文章做向量化和检索。
# how：调用 split_documents(docs) 得到切分后的 documents。
documents = text_splitter.split_documents(docs)

# what：实例化 embedding 模型。
# why：切分后的文档片段和后续 query 都要用同一个模型编码。
# how：继续使用本地模型 all-MiniLM-L6-v2。
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# what：首次建库并持久化到本地。
# why：作业 2 不只是要查，还要展示“本地向量库存储”。
# how：把 documents 和 embeddings 交给 Chroma.from_documents，同时指定 persist_directory。
db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")

# what：从本地目录重新加载 Chroma 库。
# why：这样才能真正证明这份向量库不是只存在当前内存里，而是能持久化复用。
# how：只传 persist_directory 和 embedding_function，就能把已保存的本地库重新接回来。
db2 = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


# what：程序入口。
# why：测试查询逻辑只在直接运行当前脚本时执行。
# how：使用 __name__ == "__main__" 判断。
if __name__ == "__main__":
    # what：准备测试问题。
    # why：用一个和 knowledge.txt 相关的 query 验证本地向量库检索效果。
    # how：把 query 赋值为“第三个故事是什么？”。
    query = "第三个故事是什么？"

    # what：执行相似度检索。
    # why：从本地 Chroma 向量库里找最相关的文档片段。
    # how：调用重新加载后的 db2.similarity_search(query)。
    docs = db2.similarity_search(query)

    # what：打印第一条检索结果。
    # why：最小版本先看 Top1 是否和 query 相关。
    # how：取 docs[0] 的 page_content 输出。
    print(docs[0].page_content)
