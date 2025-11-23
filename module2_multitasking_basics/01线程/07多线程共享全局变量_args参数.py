import threading
import time

num = [0]


def test1(temp):
    temp.append(33)
    print('-------------in test1 temp=%s--------' % str(temp))


def test2(temp):
    print('-------------in test2 temp=%s--------' % str(temp))

g_nums = [11,22]

def main():
    # target指定将来 这个线程去哪个函数执行代码
    # args指定将来调用 函数的时候 传递什么数据过去 格式必须为元组
    t1 = threading.Thread(target = test1,args=(g_nums,))
    t2 = threading.Thread(target = test2,args=(g_nums,))

    t1.start()
    t2.start()
    time.sleep(1)
    print(f"最终：{g_nums}")

if __name__ == "__main__":
    main()