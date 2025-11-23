import socket
import re
import time
import os

def tran_data(new_so,request):
    # 6. 接收客户端发来的请求
    recv_lines = request.splitlines()
    print('')
    print(''*20)
    print(recv_lines)

    # 7. 利用正则表达式截取出文件名
    # GET /index.html HTTP/1.1
    # file_name = re.search(r'/(.*\.*)\s',recv_lines[0])
    ret = re.match(r'[^/]+(/[^ ]*)',recv_lines[0])

    # 8. 打开文件
    if ret:
        file_name = ret.group(1)
        # print('*' * 50 , file_name)
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
    tcp_sever.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    # 2. 绑定端口
    tcp_sever.bind(('',7788))

    # 3. 监听模式
    tcp_sever.listen(128)
    tcp_sever.setblocking(False)  # 将套接字变为非堵塞 并不会直接报错 只有调用.accept()时且没有新的客户的链接才会报错

    client_socket_list = list()
    while True:
        time.sleep(2)
        try:
            # 4. 创建新的套接字 专门服务某个客户端
            new_so,addr = tcp_sever.accept()
        except Exception as ret:
            pass
        else:
            new_so.setblocking(False)
            client_socket_list.append(new_so)


        for client_socket in client_socket_list:
            try:
                recv_data = client_socket.recv(1024).decode('utf-8')
            except Exception as ret:
                pass
            else:
                if recv_data:
                    tran_data(client_socket,recv_data)
                else:
                    print('----客户端关闭了连接---')
                    client_socket.close()
                    client_socket_list.remove(client_socket)
                


        # 5. 调用传输函数
         # tran_data(new_so)

    # 6. 关闭监听套接字
    tcp_sever.close()


if __name__ == '__main__':
    main()