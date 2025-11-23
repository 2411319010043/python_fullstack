import socket


def main():
    # 1. 创建套接字 -- 用来监听
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 绑定端口
    tcp_server_socket.bind(('127.0.0.1',9090))

    # 3. 设为监听状态 负责等待新的客户端进行连接
    tcp_server_socket.listen(128) # 128指的是等待队列的最大长度
    while True: # 循环为多个客户端服务
        # 4. 等待客户端的连接 accept产生新的套接字 用来为客户端服务
        new_client_socket,client_addr = tcp_server_socket.accept() # new_client_socket是新的套接字对象 用来服务客户端 client_addr 用来存放 客户端的地址

        print(client_addr)
        print(new_client_socket)
        while True: # 循环多次为一个客户端服务
            # 接收客户端发送过来的请求数据
            recv_data = (new_client_socket.recv(1024)).decode('utf-8') # 解堵塞有两种情况：1.客户端发来了新的请求 2.客户端关闭了连接
            """
                                accept()           vs           recv()      阻塞区别总结
                特性            accept()	                    recv()
                作用对象	    监听套接字                      已连接套接字
                            tcp_server_socket	            new_client_socket
                等待目标	等待新客户端建立连接	        等待已连接客户端发送数据
                解阻塞条件	1. 有新客户端连接请求            1. 客户端发送了数据
                           2. 套接字被关闭                 2. 客户端正常关闭连接
                                                          3. 连接异常断开
                返回值	(new_socket, client_address)	    数据字节 或 空字节 b''
                后续处理	创建新的通信套接字	            处理接收到的数据

            """
            print(recv_data)
            if recv_data :
                
                # 给客户端回消息
                return_data = input('你要回复给客户端的消息：')
                new_client_socket.send(return_data.encode('utf-8'))
            else:
                break
        # 关闭
        new_client_socket.close()

    tcp_server_socket.close()





if __name__ == '__main__':
    main()



