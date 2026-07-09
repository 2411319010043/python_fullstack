# what：导入递归字符切分器
# why：长文本不能整篇拿去检索，需要先切成更小的块
# how：从 langchain_text_splitters 导入 RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# what：读取原始长文本
# why：这个例子直接演示“字符串怎么切分”，不走 loader
# how：用 open(...).read() 读出 knowledge.txt
with open("../../resource/knowledge.txt", encoding="utf-8") as f:
    knowledge = f.read()
# what：创建递归切分器
# why：我们想控制每块多大，以及块和块之间保留多少上下文
# how：设置 chunk_size、chunk_overlap、length_function、is_separator_regex
text_splitter = RecursiveCharacterTextSplitter(
    # 设置一个非常小的块大小，只是为了展示。
    chunk_size=100,
    # 块之间的目标重叠。重叠的块有助于在上下文分割时减少信息丢失。
    chunk_overlap=20,
    # 确定块大小的函数。
    # length_function 决定“块有多长”是按什么标准来算。
    # len：切分器用 Python 自带的 len() 函数来计算一段文本有多长
    length_function=len,
    # 分隔符列表（默认为 ["\n\n", "\n", " ", ""]）是否应被解释为正则表达式。
    is_separator_regex=False,
)

# what：把原始字符串切成 Document 块
# why：knowledge 现在还是字符串，不是 Document 列表，所以适合 create_documents
# how：调用 text_splitter.create_documents([knowledge])
texts = text_splitter.create_documents([knowledge])
print(texts[0])
print(texts[1])

print(text_splitter.split_text(knowledge)[:2])
