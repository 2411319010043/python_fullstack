#一、实现进程间通信的方法
    #1.socket
    #2.通过读写硬盘上的同一个文件(效率极低)
    #3.Queue队列

#二、通过Queue队列实现进程间的通信

import multiprocessing

q = multiprocessing.Queue(3)

q.put('111')

q.put(222)

q.put([11,22,33])

q.get()

q.get()

q.get()

q.get() # 堵塞 没有数据就一直等 直到有数据进来

q.get_nowait()  # 没有数据直接报错 不等

q.full() # 判断是否满了

q.empty() # 判断是否空了