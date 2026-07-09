# what：导入 HTML 加载器
# why：html 里有很多标签，不能像普通 txt 一样直接读
# how：使用 UnstructuredHTMLLoader 提取网页正文
from langchain_community.document_loaders import UnstructuredHTMLLoader

import os

BASE_DIR = os.path.dirname(__file__)

# what：指定要读取的 html 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/content.html")
)
# what：创建 HTML 加载器
# why：我们更想抽取正文内容，而不是保留整页 html 壳子
# how：传入 html 文件路径和编码方式实例化 loader
loader = UnstructuredHTMLLoader(file_path, encodings="UTF-8")

# what：加载 html 内容
# why：把网页内容转换成统一的 Document 结构，方便后续切分和检索
# how：调用 loader.load()
data = loader.load()
print(data)
