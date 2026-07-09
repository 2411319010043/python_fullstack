# what：导入 CSV 文件加载器
# why：我们要把 csv 表格内容读成 LangChain 能处理的 Document
# how：从 langchain_community.document_loaders.csv_loader 导入 CSVLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

import os

BASE_DIR = os.path.dirname(__file__)

# what：指定要读取的 csv 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/doc_search.csv")
)

# what：给 CSVLoader 传入自定义 csv_args
# why：有些 csv 可能没有合适表头，或者我们想自己指定分隔符和列名
# how：通过 csv_args 传 delimiter 和 fieldnames
loader = CSVLoader(
    file_path=file_path,
    encoding="UTF-8",
    csv_args={
        # 控制"这一行里的数据，是按什么符合分开的"
        "delimiter": ",",
        # quotechar: 表示在解析CSV文件时，使用双引号 " 作为字段值的引用字符
        # 比如"狮子,哺乳动物" 都被双引号包围，解析器会将它们识别为单个字段，而不是多个字段。
        # page_content='Name: 狮子,哺乳动物
        #"quotechar": '"',
        # 控制“每一列叫什么名字”，也就是给每列数据配一个字段名，后面程序就知道这一列代表什么。
        "fieldnames": ["Name", "Species", "Age", "Habitat"],
    },
)

# what：加载自定义解析后的 csv
# why：验证手动指定列名后，Document 会怎么生成
# how：调用 loader.load() 得到 Document 列表
data = loader.load()

for record in data[:2]:
    print(record)
