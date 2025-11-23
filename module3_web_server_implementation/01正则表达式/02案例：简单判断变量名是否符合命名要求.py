# 练习题 匹配出列表中的变量名是否有效
import re

names = ['age','_age','1age','age1','a_age','age_1_','age!','a#123','_____']
def main():
    for name in names:
        # ret = re.match(r'[a-zA-Z_]+[a-z0-9A-Z_]*',name)  .match()只会判断开头 非强制判断
        ret = re.match(r'[a-zA-Z_]+[a-z0-9A-Z_]*$',name) # $ 判断以...结尾
        if ret:
            print('变量名 %s 符合要求' % ret.group())
        else:
            print('变量名 %s 非法' % name)


if __name__ == '__main__':
    main()