# what：导入 PDF 加载器
# why：pdf 天然有分页和版式结构，不能用普通文本方式粗暴读取
# how：使用 PyPDFLoader 读取 pdf
from langchain_community.document_loaders import PyPDFLoader
import os

BASE_DIR = os.path.dirname(__file__)

# what：指定要读取的 pdf 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/pytorch.pdf")
)

# what：创建 PDF 加载器
# why：告诉程序要读取哪一个 pdf 文件
# how：把文件路径传给 PyPDFLoader
loader = PyPDFLoader(file_path)

# what：加载并切分 pdf
# why：pdf 就算按页读取，很多时候粒度还是太粗，所以这里顺手做了切分
# how：调用 loader.load_and_split() 得到切好的 Document 列表
pages = loader.load_and_split()

# what：打印第一个切分结果
# why：观察 pdf 被读出来后的 Document 长什么样
# how：打印 pages[0]
print(pages[0])