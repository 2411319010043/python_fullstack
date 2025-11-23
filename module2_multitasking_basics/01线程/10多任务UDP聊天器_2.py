import socket
import threading
import time


def send_u1(u1_socket):
    while True:

        u_send_data = input('请输入你要发送的信息：')
        if u_send_data == 'exit':
            u1_socket.close()
        u1_socket.sendto(u_send_data.encode('utf-8'),('127.0.0.1',9090))



def recv_u1(u1_socket):
    while True:
        u_recv_data,u2_addr = u1_socket.recvfrom(1024)
        mutex.acquire()
        print( '%s:%s' %(u2_addr,u_recv_data.decode('utf-8')))
        mutex.release()
    



mutex = threading.Lock()


def main():
    u1_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    u1_socket.bind(('',8080))  #接收元组形式

    t1 = threading.Thread(target= send_u1,args=(u1_socket,))
    t2 = threading.Thread(target= recv_u1,args=(u1_socket,))
    t1.start()
    t2.start()



if __name__ == '__main__':
    main()




"""UDP套接字流程
1.创建套接字
2.绑定端口
3.收发消息
4.关闭套接字"""