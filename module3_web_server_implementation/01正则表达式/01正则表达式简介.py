import re

# re.match(正则表达式，需要处理的字符串)

print(re.match(r'hello','hello world'))

print(re.match(r'hello','Hello world'))

print(re.match(r'[hH]ello','hello world'))

# 一、 匹配单个字符
ret = re.match(r'速度与激情\d','速度与激情6') # \d 匹配单个数字(0-9)
print(ret.group())

print(re.match(r'速度与激情\w','速度与激情哈').group()) # 匹配单个字符(a-z,A-Z,0-9,_,中文,英文,日文等......)

print(re.match(r'速度与激情\s','速度与激情 ').group()) # 匹配空格，tab键 

ret = re.match(r'速度与激情[0-8]','速度与激情0') # 匹配0到8的数字
print(ret.group())

print(re.match(r'速度与激情[1-36-8]','速度与激情2').group()) # 匹配1到3，6到8

print(re.match(r'速度与激情[1-8a-zA-Z]','速度与激情Z').group()) # 匹配1到8，a到z,A到Z

print(re.match(r'速度与激情.','速度与激情Z').group()) # 匹配所有字符除了\n


# 二、 匹配多个字符
    # {}可以限制 前面紧挨着的这个条件可以有几个
print(re.match(r'速度与激情\d{1,2}','速度与激情99').group()) # 匹配\d可以有1个或两个 可以是一位数字也可以是两位数字

print(re.match(r'速度与激情\d{1,3}','速度与激情999').group()) # 匹配\d可以有1个2个或3个 可以是一位数字也可以是两位数字还可以是三位数字

print(re.match(r'\d{11}','12345678901').group()) # 匹配11位电话号码

    # ？前面的一位可以有一个也可以没有
print(re.match(r'021-?\d{8}','02112345678').group()) # 匹配北京市号码 -可以有也可以没有

print(re.match(r'\d{3,4}-?\d{8}','053112345678').group()) # 匹配北京市号码 -可以有也可以没有

    # * 前面的一位可以没有 可以有一个 可以有多个
print(re.match(r'\d{3,4}-?\d{8}','053112345678').group()) # 匹配北京市号码 -可以有也可以没有

html_content = """fdsf
                    aaaa
                    bbbb
                    cccc"""
print(re.match(r'.*',html_content).group()) # .匹配不到\n

print(re.match(r'.*',html_content,re.S).group()) # 后面传入re.S参数能匹配到\n

print(re.match(r'.*','').group()) # 匹配空白字符

    # +前面的一位可以有一个或多个 但是不能没有

# print(re.match(r'.+','').group())  # 报错
print(re.match(r'.+','a').group()) 



