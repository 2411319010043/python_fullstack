import threading
import time


class MyThread(threading.Thread): # 继承Thrad类
    def run(self): 
        for i in range(3):
            time.sleep(1)
            print(i)

    #其他函数...


if __name__ == '__main__':
    t = MyThread()  #直接实例化类
    t.start()  #调用start()函数接下来回自动调用run() 










    