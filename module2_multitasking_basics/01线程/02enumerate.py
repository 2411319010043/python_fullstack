"""
enumerate : 在遍历一个序列（如列表、元组、字符串）的同时，自动提供一个计数值（索引）。
         “带编号的遍历”
"""

names = ['aa','bb','cc']

for temp in names:
    print(temp)


for temp in enumerate(names): 
    print(temp,type(temp))
    

# 可以进行拆包
for i,temp in enumerate(names):
    print(f'第{i}个：{temp}')