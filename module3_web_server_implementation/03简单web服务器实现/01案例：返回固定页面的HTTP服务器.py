'''
1.TCP服务器 
    绑定端口
    等待接收
    接收到了就创建一个接口为其服务
    发送数据


      ①服务器   一定要绑定端口
            导入socket模块
            创建套接字 socket.SOCK_STREAM
            绑定端口 .bind()
            设置监听模式 .listen()
            创建新的套接字 .accept()
            接收请求 .recv()
            发送数据 .send()
            关闭新的套接字 .close()
            关闭监听的套接字
'''

import socket


def service_client(new_socket):
    '''为这个客户端返回数据'''
    # 1. 接收浏览器发送过来的请求，即HTTP请求
    request = new_socket.recv(1024)
    print(request)

    # 2. 返回HTTP格式的数据，给浏览器
    # 2.1 准备发送给浏览器的数据...header     浏览器能够解析的换行: \r\n
    response = 'HTTP/1.1 200 OK\r\n'
    response += '\r\n'
    # 2.2 准备发送给浏览器的数据...body
    response += '<h1>hahaha</h1>'
    new_socket.send(response.encode('utf-8'))

    # 3. 关闭套接字
    new_socket.close()

def main():
    '''用来完成整体的控制'''
    # 1. 创建套接字
    tcp_sever = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 绑定
    tcp_sever.bind(('',8081))

    # 3. 变为监听套接字
    tcp_sever.listen(128)
    while True:
        # 4. 等待新客户端的链接
        new_socket,client_addr = tcp_sever.accept()

        # 5. 为这个客户端服务
        service_client(new_socket)
    
    # 关闭监听套接字
    tcp_sever.close()


if __name__ == '__main__':
    main()