# 案例：匹配html标签
import re

# 例1：
html_str = '<h1>hahaha</h2>'
ret = re.match(r'<\w*>.*</\w*>$',html_str) # 若前后数字不一致并不能筛选出来

html_str2 = '<h1>hahaha</h2>'
ret = re.match(r'<(\w*)>.*</\1>$',html_str2) # 利用分组可以筛选出来
print(ret)

# 例2：
html_str3 = '<body><h1>hahah</h1></body>'
ret = re.match(r'<(\w*)><(\w*)>.*</\2></\1>',html_str3)
print(ret)



