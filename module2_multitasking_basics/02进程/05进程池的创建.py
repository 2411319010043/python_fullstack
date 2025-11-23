from multiprocessing import Pool # 1. 导入模块
import os,time,random


def worker(msg):
    t_start = time.time()
    print('%s开始执行，进程号为%d' % (msg,os.getpid()))

    # random.random() 随机生成0-1之间的浮点数
    time.sleep(random.random()*2)
    t_stop = time.time()
    print(msg,'执行完毕，耗时%0.2f' % (t_stop - t_start))

def main():
    po = Pool(3) # 2. 实例化进程池，最大进程数3

    for i in range(0,10):
        # Pool().apply_async(要调用的目标名,(要传递给目标的参数元组,))
        #每次循环将会用空闲出来的子进程去调用目标
        po.apply_async(worker,(i,))
    
    print('--------start--------')
    po.close() # 关闭进程池 关闭后po不再接收新的请求 close()必须在join()的前面
    po.join() # 等待po中所有子进程执行完成，必须放在close语句之后 
              # 不写join 主进程执行完所有的代码后直接死亡 不会等待子进程
    print('--------end---------')
    

if __name__ == '__main__':
    main()