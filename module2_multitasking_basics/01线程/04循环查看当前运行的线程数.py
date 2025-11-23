import time
import threading


#线程执行的顺序不确定


def test1():
    for i in range(5):
        print('-----test1---%d',i)
        time.sleep(1)

    # 如果创建thread时执行的函数运行结束，那么子线程也会随之消失

def test2():
    for i in range(5):
        print('-----test2---%d',i)
        time.sleep(1)

def main():
    t1 = threading.Thread(target= test1)
    t2 = threading.Thread(target= test2)
    t1.start() # 调用Thread的时候不会创建线程 调用start() 才会创建线程以及线程开始执行
    t2.start()
    while True:
        print(threading.enumerate())
        time.sleep(1)
        if len(threading.enumerate()) == 1:
            break


if __name__ == '__main__':
    main()