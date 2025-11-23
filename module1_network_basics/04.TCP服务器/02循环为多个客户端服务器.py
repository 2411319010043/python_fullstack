import socket


def main():
    # 1. 创建套接字 -- 用来监听
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 绑定端口
    tcp_server_socket.bind(('127.0.0.1',8080))

    # 3. 设为监听状态 负责等待新的客户端进行连接
    tcp_server_socket.listen(128)
    while True:
        # 4. 等待客户端的连接 accept产生新的套接字 用来为客户端服务
        new_client_socket,client_addr = tcp_server_socket.accept() # new_client_socket是新的套接字对象 用来服务客户端 client_addr 用来存放 客户端的地址

        print(client_addr)
        print(new_client_socket)

        #接收客户端发送过来的请求数据
        recv_data = (new_client_socket.recv(1024)).decode('utf-8')
        print(recv_data)

        #给客户端回消息
        new_client_socket.send('hhhh'.encode('utf-8'))

        # 关闭
        new_client_socket.close()

    tcp_server_socket.close()





if __name__ == '__main__':
    main()



"""

recv()和recvfrom()的区别
特性	      recv()	    recvfrom()
协议类型	TCP (面向连接)	UDP (无连接)
返回值	     只有数据	   (数据, 地址)元组
连接要求	需要先建立连接	  不需要连接
使用场景	流式数据传输	  数据报传输

"""

