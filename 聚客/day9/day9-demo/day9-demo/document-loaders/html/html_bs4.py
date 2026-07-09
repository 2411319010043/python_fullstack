# what：导入基于 BeautifulSoup 的 HTML 加载器
# why：同样是读 html，不同 loader 的提取风格和 metadata 保留方式可能不同
# how：使用 BSHTMLLoader 读取 html
from langchain_community.document_loaders import BSHTMLLoader
import os

BASE_DIR = os.path.dirname(__file__)
# what：指定要读取的 html 文件路径
# why：加载器需要知道要读取哪一个文件
# how：把资源文件路径保存到 file_path 变量中
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "../../resource/content.html")
)
# what：创建 BSHTMLLoader
# why：演示 html 还能用另一种方式提取，并且可能保留 title 等 metadata
# how：传入文件路径和编码方式
loader = BSHTMLLoader(file_path, open_encoding="UTF-8")
# what：加载 html 并打印结果
# why：对比它和 UnstructuredHTMLLoader 的输出差异
# how：调用 load() 后直接打印
data = loader.load()
print(data)
