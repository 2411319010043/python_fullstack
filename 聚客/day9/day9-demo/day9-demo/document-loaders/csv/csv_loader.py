# what: 导入 CSV 文件加载器，按表格结构去读 CSV
# why: 我们要把 csv 表格内容读成 LangChain 能处理的 Document
# how: 从 langchain_community.document_loaders.csv_loader 导入 CSVLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

import os

BASE_DIR = os.path.dirname(__file__)

# what：指定要读取的 csv 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/doc_search.csv")
)

# what：创建 CSV 加载器
# why：不同文件类型要用对应的 loader，csv 不能直接拿 html/pdf 的 loader 来读
# how：传入文件路径和编码方式，实例化 CSVLoader
loader = CSVLoader(file_path=file_path,encoding="UTF-8")

# what：真正加载 csv 文件内容
# why：前面的 loader 只是创建工具，这一步才会把文件读出来
# how：调用 loader.load()，返回 Document 列表
data = loader.load()

# what：打印前两条加载结果
# why：先观察 Document 长什么样，避免一下子打印太多内容
# how：切片取前两条，再逐条打印
for record in data[:2]:
    print(record)
