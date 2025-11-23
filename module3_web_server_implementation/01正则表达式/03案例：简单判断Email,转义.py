# 匹配出163的邮箱地址，且@符合之前有4-20位 包含数字字母下划线 例如：hello@163.com
import re


def main():
    email = input('请输入邮箱地址：')
    # 若在正则表达式中需要用到某些特殊的字符 如：. ? + 等 需要在前面加上\ 即\. \+
    # ret = re.match(r'[0-9a-zA-Z_]{4,20}@163\.com$',email)

    # 优化 不仅可以判断163.com还可以判定126.com
    ret = re.match(r'([0-9a-zA-Z_]{4,20})@(163|126|qq|gemail)\.com$',email)
    

    if ret:
        print('你输入的地址正确：%s' % email)
        print('这个邮箱地址属于：%s' % ret.group(2)) # 将要单独提取出的信息加上()然后用.group(第几个括号) 就可以单独显示提取出的信息 例如：分类邮箱
        print('这个邮箱的命名是：%s' % ret.group(1)) 
    else:
        print('你输入的地址有误：%s' % email)



if __name__ == '__main__':
    main()
