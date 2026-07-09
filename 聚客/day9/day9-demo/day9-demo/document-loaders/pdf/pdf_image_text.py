# what：创建支持提取图片内容的 PDF 加载器
# why：有些 pdf 的文字其实在图片里，普通提取可能拿不全
# how：给 PyPDFLoader 传 extract_images=True
from langchain_community.document_loaders import PyPDFLoader

import os

BASE_DIR = os.path.dirname(__file__)

# what：指定要读取的 pdf 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/pytorch.pdf")
)

# what：加载 pdf 内容
# why：把图片中的文字也尽量识别进知识库
# how：调用 loader.load()
loader = PyPDFLoader(file_path, extract_images=True)
pages = loader.load()
# what：打印某一页的内容
# why：验证图片文字是否被提取出来
# how：打印 pages[8].page_content
print(pages[8].page_content)