# what：导入 Path。
# why：优化版仍然需要稳定定位 knowledge.txt 的文件路径。
# how：通过脚本自身位置拼出知识库绝对路径。
from pathlib import Path

# what：导入 Chroma。
# why：这份优化版仍然基于本地 Chroma 向量库完成检索。
# how：使用 langchain_chroma 提供的 Chroma 类。
from langchain_chroma import Chroma

# what：导入文本加载器。
# why：优化检索效果之前，仍然要先把知识库从磁盘读进来。
# how：使用 TextLoader 读取 txt。
from langchain_community.document_loaders import TextLoader

# what：导入字符切分器。
# why：优化版的关键之一就是把文档切得更细。
# how：继续使用 CharacterTextSplitter，但调整参数。
from langchain_text_splitters import CharacterTextSplitter

# what：导入 HuggingFace embedding 封装器。
# why：切分后的文档块和 query 仍然要先转成向量。
# how：继续使用 all-MiniLM-L6-v2。
from langchain_huggingface import HuggingFaceEmbeddings

# what：获取当前脚本目录。
# why：方便稳定拼接 knowledge.txt 的位置。
# how：使用 Path(__file__).resolve().parent。
base_dir = Path(__file__).resolve().parent

# what：拼出知识库路径。
# why：避免因为终端工作目录不同导致找不到文件。
# how：从 homework 目录回到上一级，再进入 resource/knowledge.txt。
knowledge_path = base_dir.parent / "resource" / "knowledge.txt"

# what：创建文本加载器。
# why：定义要加载哪份知识库和编码方式。
# how：把 knowledge_path 转成字符串传给 TextLoader。
loader = TextLoader(str(knowledge_path), encoding="UTF-8")

# what：读取知识库内容。
# why：后面切分、建库都依赖这份原始文档数据。
# how：调用 loader.load() 得到 docs。
docs = loader.load()

# what：创建优化版切分器。
# why：原版粒度太粗，检索“第三个故事是什么”时容易只命中大段相关内容而不够精确。
# how：把块大小调小到 500，并增加 100 个字符的重叠来保留上下文连续性。
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# what：切分原始文档。
# why：把大文章拆成更细的片段后，检索会更容易命中真正相关的局部内容。
# how：调用 split_documents(docs) 得到 documents。
documents = text_splitter.split_documents(docs)

# what：实例化 embedding 模型。
# why：优化版仍然需要把文档块和 query 放进同一个向量空间。
# how：继续用 all-MiniLM-L6-v2。
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# what：建库并写入优化版本地目录。
# why：避免和标准版共用同一个目录，防止混淆两套不同切分策略的结果。
# how：指定 persist_directory 为 ./chroma_db_optimized。
db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db_optimized")

# what：从优化版目录重新加载 Chroma 库。
# why：继续保持“先存盘，再加载，再查询”的完整闭环。
# how：用 persist_directory 和 embedding_function 重新创建一个 db2。
db2 = Chroma(persist_directory="./chroma_db_optimized", embedding_function=embeddings)


# what：程序入口。
# why：只在直接运行这个优化版脚本时执行测试查询。
# how：使用 __name__ == "__main__"。
if __name__ == "__main__":
    # what：准备测试 query。
    # why：我们要对比优化前后检索“第三个故事是什么”时的效果差异。
    # how：把 query 写成自然语言问题。
    query = "第三个故事是什么？"

    # what：执行带分数的相似度检索。
    # why：优化版不只想看内容，还想看前 3 条结果和它们的距离分数。
    # how：调用 db2.similarity_search_with_score(query, k=3)。
    docs_and_scores = db2.similarity_search_with_score(query, k=3)

    # what：遍历前三条结果。
    # why：Top1 不一定总是最理想答案，看 Top3 更方便分析检索质量。
    # how：用 enumerate 同时拿到排名、文档和分数。
    for i, (doc, score) in enumerate(docs_and_scores, start=1):
        # what：打印当前结果排名。
        # why：明确展示这是第几条检索结果。
        # how：用 f-string 输出 Top i。
        print(f"Top {i}")

        # what：打印距离分数。
        # why：Chroma 这里返回的是距离，分数越小通常代表越相似。
        # how：直接输出 score。
        print(f"score: {score}")

        # what：打印命中的文档内容。
        # why：需要看检索到的具体片段是否真的回答了 query。
        # how：输出 doc.page_content。
        print(doc.page_content)

        # what：打印分隔线。
        # why：让多条候选结果在终端里更容易区分。
        # how：输出 40 个连字符。
        print("-" * 40)
