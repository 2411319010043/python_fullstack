import gevent
import time
from gevent import monkey

monkey.patch_all() # 可以将代码中哦所有的延时操作换成 gevent.....

def f1(n):
    for i in range(n):
        print(gevent.getcurrent(),i)
        time.sleep(1) # 这种延时不可以

def f2(n):
    for i in range(n):
        print(gevent.getcurrent(),i)
        time.sleep(1)


def f3(n):
    for i in range(n):
        print(gevent.getcurrent(),i)
        time.sleep(1)


gevent.joinall([
        gevent.spawn(f1,5),
        gevent.spawn(f2,5),
        gevent.spawn(f3,5)

])
# 利用joinall(列表) 可以省去单独写xx.join()


# gevent 套用模板
'''

1. 导入模块 from gevent import monkey
          import gevent

2. 打补丁 monkey.patch_all()

3. gevent.joinall([gevent.spawn()])

'''