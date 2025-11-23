import socket

def main():
    #创建一个udp套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    #可以使用套接字收发数据
    #发送数据 ---sendto('发送的内容','元组形式的对方ip以及port')
    udp_socket.sendto(b'hhhhh',('127.0.0.1',8080))
    #关闭套接字
    udp_socket.close()

if __name__ == "__main__":
    main()



