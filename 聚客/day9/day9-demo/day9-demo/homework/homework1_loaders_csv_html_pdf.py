# 先拼路径 -> 再创建 loader -> 再 load -> 最后观察 Document
import os

# what：导入 CSV 文件加载器
# why：我们要把 csv 表格文件读成 LangChain 统一的 Document 结构
# how：从 langchain_community.document_loaders.csv_loader 导入 CSVLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

# what：导入 HTML 文件加载器
# why：我们要读取 html 文件中的正文内容
# how：使用 BSHTMLLoader 加载 html 文件
from langchain_community.document_loaders import BSHTMLLoader

# what：导入 PDF 文件加载器
# why：我们要读取 pdf 文件内容，并观察它的 page_content 和 metadata
# how：使用 PyPDFLoader 加载 pdf 文件
from langchain_community.document_loaders import PyPDFLoader

# what：获取当前作业脚本所在目录
# why：后面要基于当前脚本位置，稳定地去拼 resource 目录下的文件路径
# how：使用 os.path.dirname(__file__) 得到当前脚本目录
BASE_DIR = os.path.dirname(__file__)


print("======== CSV Loader ========")

# what：拼接 csv 资源文件的绝对路径
# why：避免因为运行目录不同而找不到文件
# how：先用 os.path.join 拼接，再用 os.path.abspath 转成绝对路径
csv_path = os.path.abspath(os.path.join(BASE_DIR,"../resource/doc_search.csv"))

# what：创建 CSV 加载器
# why：csv 文件要用对应的 loader 读取
# how：把 csv_path 和编码方式传给 CSVLoader
loader = CSVLoader(file_path=csv_path, encoding="UTF-8")

# what：加载 csv 文件内容
# why：把 csv 文件转换成 LangChain 的 Document 列表
# how：调用 loader.load()
data = loader.load()

# what：打印第一条 Document 的整体结构
# why：先整体观察 page_content 和 metadata 长什么样
# how：打印 data[0]
print(data[0])
print("=================================")
# what：打印第一条 Document 的正文内容
# why：观察 csv 一行数据被转换成了怎样的文本
# how：打印 data[0].page_content
print(data[0].page_content)
# what：打印第一条 Document 的附加信息
# why：观察 source、row 等 metadata
# how：打印 data[0].metadata
print(data[0].metadata)



print("======== HTML Loader ========")

# what：拼接 html 资源文件的绝对路径
# why：稳定定位 content.html
# how：基于 BASE_DIR 拼接 ../resource/content.html
html_path = os.path.abspath(os.path.join(BASE_DIR, "../resource/content.html"))

# what：创建 HTML 加载器
# why：html 文件包含标签结构，要用专门的 loader 读取
# how：把 html_path 和编码方式传给 BSHTMLLoader
loader = BSHTMLLoader(html_path, open_encoding="UTF-8")
# what：加载 html 文件内容
# why：把 html 文件转换成 Document 列表
# how：调用 loader.load()
data = loader.load()
# what：打印第一条 Document 的整体结构
# why：先整体看 HTML loader 的输出
# how：打印 data[0]
print(data[0])
print("=================================")
# what：打印正文内容
# why：观察 html 提取出来的文本内容
# how：打印 data[0].page_content
print(data[0].page_content)
# what：打印附加信息
# why：观察 html 的 metadata，比如 source、title
# how：打印 data[0].metadata
print(data[0].metadata)


print("======== PDF Loader ========")
# what：拼接 pdf 资源文件的绝对路径
# why：稳定定位 pytorch.pdf
# how：基于 BASE_DIR 拼接 ../resource/pytorch.pdf
pdf_path = os.path.abspath(os.path.join(BASE_DIR, "../resource/pytorch.pdf"))

# what：创建 PDF 加载器
# why：pdf 文件要用专门的 loader 读取
# how：把 pdf_path 传给 PyPDFLoader
loader = PyPDFLoader(pdf_path)

# what：加载 pdf 文件内容
# why：把 pdf 转成 Document 列表
# how：调用 loader.load()
data = loader.load()
# what：打印第一页对应的 Document 整体结构
# why：先整体观察 pdf loader 的输出
# how：打印 data[0]
print(data[0])
print("=================================")
# what：打印第一页正文内容
# why：观察 pdf 提取出来的文本
# how：打印 data[0].page_content
print(data[0].page_content)
# what：打印第一页附加信息
# why：观察 pdf 的 metadata，比如 source、page
# how：打印 data[0].metadata
print(data[0].metadata)
