import socket
import re
import select

def tran_data(new_so,request):
    # 6. 接收客户端发来的请求
    recv_lines = request.splitlines()  # 按换行符进行分割 返回列表
    print('')
    print(''*20)
    print(recv_lines)

    # 7. 利用正则表达式截取出文件名
    ret = re.match(r'[^/]+(/[^ ]*)',recv_lines[0])

    # 8. 打开文件
    if ret:
        file_name = ret.group(1)
        if file_name == '/':  # 显示默认页面
            file_name = '/index.html'

    try:   
        file = open ('./html' + file_name,'rb') 
    except:   
        response = 'HTTP/1.1 404 NOT FOUND\r\n' 
        response += '\r\n'
        response += '----------file not found-----'
        new_so.send(response.encode('utf-8'))
    else:
        # 9. 读取数据
        send_data_html = file.read()
        # 10. 关闭文件
        file.close()
        # 11. 拼接header
        response_body = send_data_html
        response_header = 'HTTP/1.1 200 OK\r\n'
        response_header += 'Content-Length:%d\r\n' % len(response_body) 
        response_header += '\r\n'
        response = response_header.encode('utf-8') + response_body

        # 12. 拼接body
        # send_data += send_data_html # 不能直接进行拼接 因为header是字符串 而读取出来的body是二进制形式
        # 13. 发送数据
        new_so.send(response)

    # 14.关闭套接字
    # new_so.close()
    

def main():
    # 1. 创建套接字
    tcp_sever = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_sever.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # 允许服务器快速重启，避免"地址已使用"的错误。

    # 2. 绑定端口
    tcp_sever.bind(('',7788))

    # 3. 监听模式
    tcp_sever.listen(128)
    tcp_sever.setblocking(False)  # 将套接字变为非堵塞

    # 创建一个epoll对象
    epl = select.epoll()

    # 将监听套接字对应的fd注册到epoll中
    epl.register(tcp_sever.fileno(),select.EPOLLIN)

    fd_event_dict = dict()  # 创建一个字典用来存放 {fd：套接字}

    while True:

        fd_event_list = epl.poll()  # 默认会堵塞，直到os检测到数据到来 通过事件通知方式告诉这个程序，此时才会解堵塞 返回值是列表嵌套元组
        #[(fd,event),(套接字对应的文件描述符，这个描述符到底是什么事件 例如: 可以调用recv接收等)]

        for fd,event in fd_event_list:
            # 等待新客户端的链接
            if fd == tcp_sever.fileno():  # 筛选出是否是监听套接字所接收到的新客户端的链接
                new_so,addr = tcp_sever.accept()  # 如果是 就派新的套接字专门服务新客户端
                epl.register(new_so.fileno(),select.EPOLLIN) # 把新的套接字fd给epoll
                fd_event_dict[new_so.fileno()] = new_so # 存入字典中
            elif event == select.EPOLLIN:
                # 判断已经链接的客户端是否有数据发送过来
                recv_data = fd_event_dict[fd].recv(1024).decode('utf-8')

                if recv_data:
                    tran_data(fd_event_dict[fd],recv_data)
                else:
                    fd_event_dict[fd].close()
                    epl.unregister(fd)  # 注销epoll中的fd
                    del fd_event_dict[fd]  # 删除字典中的fd对应的键值对
        # 5. 调用传输函数
         # tran_data(new_so)

    # 6. 关闭监听套接字
    tcp_sever.close()


if __name__ == '__main__':
    main()