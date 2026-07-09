import os

# what：导入递归字符切分器
# why：我们要演示如何按文本结构和字符边界切分长文本
# how：从 langchain_text_splitters 导入 RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# what：导入语义切分器
# why：我们要演示如何根据语义变化来切分长文本
# how：从 langchain_experimental.text_splitter 导入 SemanticChunker
from langchain_experimental.text_splitter import SemanticChunker

# what：导入 HuggingFace 向量模型封装器
# why：语义切分需要先比较句子之间的语义相似度，所以要先有 embedding 模型
# how：从 langchain_huggingface 导入 HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

# what：获取当前作业脚本所在目录
# why：后面要基于当前脚本位置稳定地找到 resource 目录下的文本文件
# how：使用 os.path.dirname(__file__) 得到当前脚本目录
BASE_DIR = os.path.dirname(__file__)

# what：拼接知识库文本文件的绝对路径
# why：避免因为终端运行位置不同而找不到知识库文件
# how：先用 os.path.join 拼接路径，再用 os.path.abspath 转成绝对路径
path = os.path.abspath(os.path.join(BASE_DIR, "../resource/knowledge.txt"))

# what：读取原始长文本
# why：这次作业的重点是 splitter，所以直接拿原始字符串更方便演示 create_documents
# how：使用 open(...).read() 读取 knowledge.txt 的全部内容
with open(path, encoding="utf-8") as f:
    knowledge = f.read()


print("========= RecursiveCharacterTextSplitter =======")

# what：创建递归字符切分器
# why：我们要把长文本切成更适合检索和观察的小块
# how：设置 chunk_size 控制块大小，chunk_overlap 控制块之间的重叠部分
recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

# what：把原始字符串切分成 Document 列表
# why：knowledge 现在是原始字符串，所以更适合使用 create_documents
# how：调用 recursive_splitter.create_documents([knowledge])
texts = recursive_splitter.create_documents([knowledge])

# what：打印前两个切分结果
# why：方便观察递归切分后的 chunk 内容长什么样
# how：使用 enumerate 同时拿到编号和每个 Document，再打印 page_content
for i, doc in enumerate(texts[:2], start=1):
    print(f"========  Chunk {i} ========")
    print(doc.page_content)

# what：打印递归切分后的总块数
# why：方便观察这次切分一共切出了多少段
# how：使用 len(texts) 统计总块数
print(len(texts))


print("========= SemanticChunker =======")

# what：实例化语义切分要用的 embedding 模型
# why：SemanticChunker 需要先根据向量比较句子之间的语义差异
# how：使用本地 HuggingFace 模型 all-MiniLM-L6-v2
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# what：创建语义切分器
# why：我们想按语义变化来切分，而不是只按字符长度来切
# how：传入 embedding 模型，并额外设置适合中文文本的分句规则和切分阈值
semantic_splitter = SemanticChunker(
    embeddings,
    sentence_split_regex=r"(?<=[。！？])",
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=50,
    min_chunk_size=50,
)

# what：按语义切分原始长文本
# why：观察语义切分和递归切分的结果差异
# how：调用 semantic_splitter.create_documents([knowledge])
texts = semantic_splitter.create_documents([knowledge])

# what：打印前两个语义切分结果
# why：方便观察语义切分后的 chunk 是否更贴近完整语义
# how：使用 enumerate 同时拿到编号和每个 Document，再打印 page_content
for i, doc in enumerate(texts[:2], start=1):
    print(f"========  Chunk {i} ========")
    print(doc.page_content)

# what：打印语义切分后的总块数
# why：方便观察语义切分一共生成了多少段
# how：使用 len(texts) 统计总块数
print(len(texts))
