import threading
import time

g_num = 0


def test1(num):
    global g_num
    
    for i in range(num):
        mutex.acquire()
        g_num += 1
        mutex.release()
    print('-------test1 g_num=%d---' % g_num)  
    # 为什么-------test1 g_num=1957218---? 因为 g_num是全局变量 test1 打印的是它执行完成时刻的值，不是最终值


def test2(num):
    global g_num
    for i in range(num):
        mutex.acquire()
        g_num += 1
        mutex.release()
    print('-------test1 g_num=%d---' % g_num)

# 创建一个互斥锁，默认是没有上锁的
mutex = threading.Lock()

def main():

    t1 = threading.Thread(target = test1,args=(1000000,))
    t2 = threading.Thread(target = test2,args=(1000000,))

    t1.start()
    t2.start()
    time.sleep(5)
    print(f"最终：{g_num}")


if __name__ == "__main__":
    main()