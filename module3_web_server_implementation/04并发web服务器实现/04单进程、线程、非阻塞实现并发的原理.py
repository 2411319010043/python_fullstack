import socket
import time

def main():
    tcp_sever_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    tcp_sever_tcp.bind(('',7899))

    tcp_sever_tcp.listen(128)

    tcp_sever_tcp.setblocking(False) # 设置套接字为非堵塞的方式

    client_socket_list = list()

    while True:
        time.sleep(1)
        try:
            new_socket,new_addr = tcp_sever_tcp.accept()
        except Exception as ret:
            print('----没有新的客户端到来----')
        else:
            print('----只要没有产生异常，那么也就意味着，来了一个新的客户端---')
            new_socket.setblocking(False) # 设置套接字为非堵塞的方式
            client_socket_list.append(new_socket)

        for client_socket in client_socket_list:
            try:
                recv_data = client_socket.recv(1024)
            except Exception as ret:
                print(ret)
                print('---这个客户没有发送数据过来---')
            else:
                if recv_data:
                    # 对方发送过来数据
                    print('----客户端发送过来了数据-----')
                    print(recv_data)
                else:
                    # 对方调用close 导致recv返回
                    client_socket_list.remove(client_socket) # 移除该client_socket
                    client_socket.close() # 客户端关闭 服务该客户端的套接字也就关闭了
                    print('---客户端已经关闭---')
                

if __name__ == '__main__':
    main()