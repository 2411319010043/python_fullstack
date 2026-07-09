# pip install -qU langchain-text-splitters

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载示例文档
with open("../../resource/knowledge.txt", encoding="utf-8") as f:
    knowledge = f.read()
# what：手动指定分隔符列表
# why：不同语言和文本格式的自然边界不同，默认分隔符不一定够用
# how：通过 separators 参数手动传入换行、空格、英文标点、中文标点和兜底空字符串
text_splitter = RecursiveCharacterTextSplitter(
    # 设置一个非常小的块大小，只是为了展示。
    chunk_size=100,
    # 块之间的目标重叠。重叠的块有助于在上下文分割时减少信息丢失。
    chunk_overlap=20,
    # 确定块大小的函数。
    length_function=len,
    # 分隔符列表（默认为 ["\n\n", "\n", " ", ""]）是否应被解释为正则表达式。
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # 零宽空格
        "\uff0c",  # 全角逗号
        "\u3001",  # 表意逗号
        "\uff0e",  # 全角句号
        "\u3002",  # 表意句号
        "",
    ],
)
# what：按自定义分隔符进行切分
# why：让中文文本切得更自然，减少退化成硬切的概率
# how：调用 create_documents([knowledge])
texts = text_splitter.create_documents([knowledge])
print(texts[0])
print(texts[1])

print(text_splitter.split_text(knowledge)[:2])
