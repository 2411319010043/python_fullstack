import re


# 一、 search 不用从头开始匹配
ret = re.search(r'\d+','阅读次数为：9999').group()
print(ret)
ret = re.search(r'\d+','阅读次数为：9999,点赞数为：100').group() # 但只会找出第一次匹配成功的
print(ret)

# 二、 findall 返回值是列表 可以找出所有匹配成功的结果
ret = re.findall(r'\d+','阅读次数为：9999,点赞数为：100') 
print(ret)

# 三、 sub 将匹配到的数据进行替换
# sub(r'正则表达式','要替换的数据','被替换的数据')
ret = re.sub(r'\d+','998','python = 222') 
print(ret)

# 四、 split根据匹配进行切割 返回列表
ret = re.split(r':| ','info:xiaoZhang 33 shandong')
print(ret)










