import socket

def main():
    pass
    # 1. 创建tcp的套接字
    tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 链接服务器
    server_ip = input('请输入连接服务器的IP')
    server_port = int(input('请输入连接服务器的port'))
    server_addr = (server_ip,server_port)
    tcp_socket.connect(server_addr) #  接收元组形式
    while True:
        # 3.1  发送数据
        send_data = input('请输入要发送的数据：')
        if send_data == 'exit':
            break
        tcp_socket.send(send_data.encode('utf-8'))
        # 3.2  接收数据
        recv_data = (tcp_socket.recv(1024)).decode('utf-8')
        print(recv_data)



    # 4. 关闭套接字
    tcp_socket.close()


if __name__ == '__main__':
    main()












