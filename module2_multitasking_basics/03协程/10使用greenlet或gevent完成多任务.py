import gevent


def f1(n):
    for i in range(n):
        print(gevent.getcurrent(),i)
        #time.sleep(1) 这种延时不可以
        gevent.sleep(0.5)

def f2(n):
    for i in range(n):
        print(gevent.getcurrent(),i)
        #time.sleep(1)
        gevent.sleep(0.5)

def f3(n):
    for i in range(n):
        print(gevent.getcurrent(),i)
        #time.sleep(1)
        gevent.sleep(0.5)

print('---1---')
g1 = gevent.spawn(f1,5)
print('---2---')
g2 = gevent.spawn(f2,5)
print('---3---')
g3 = gevent.spawn(f3,5)
print('---4---')
g1.join()
g2.join()
g3.join()

 # 协程就是利用单线程耗时操作去干别的事情 协程依赖于线程，线程依赖于进程
