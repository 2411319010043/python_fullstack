import time
import threading


def sing():
    ''' 唱歌 5s'''
    for i in range(5):
        print('---正在唱菊花茶---')
        time.sleep(1)


def dance():
    ''' 跳舞 5s'''
    for i in range(5):
        print('---正在跳舞---')
        time.sleep(1)


def main():
    t1 = threading.Thread(target= sing) # 调用threading模块中的Thread类 实例化出t1对象 并指向函数 sing
    t2 = threading.Thread(target= dance)
    t1.start() #执行start()函数的时候 由主线程衍生出一个子线程 并执行t1所指向的函数
    t2.start()


if __name__ == '__main__':
    main()

    