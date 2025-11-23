import socket
import re
import multiprocessing

road = 'module3_web_server_implementation\03简单web服务器实现\html'

def tran_data(new_so):

    # 6. 接收客户端发来的请求
    recv_data = new_so.recv(1024).decode('utf-8')
    # print('>>>>'*50)
    # print(recv_data)
    recv_lines = recv_data.splitlines()
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
        send_data = 'HTTP/1.1 404 NOT FOUND\r\n'
        send_data += '\r\n'
        send_data += '----------file not found-----'
        new_so.send(send_data.encode('utf-8'))

    else:
        # 9. 读取数据
        send_data_html = file.read()

        # 10. 关闭文件
        file.close()

        # 11. 拼接header
        send_data = 'HTTP/1.1 200 OK\r\n'
        send_data += '\r\n'

        # 12. 拼接body
        # send_data += send_data_html # 不能直接进行拼接 因为header是字符串 而读取出来的body是二进制形式
        
        # 13. 发送数据
        new_so.send(send_data.encode('utf-8'))
        new_so.send(send_data_html) # 直接发送两次

    # 14.关闭套接字
    new_so.close()
    


def main():
    # 1. 创建套接字
    tcp_sever = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 绑定端口
    tcp_sever.bind(('',7788))

    # 3. 监听模式
    tcp_sever.listen(128)
    while True:
        # 4. 创建新的套接字 专门服务某个客户端
        new_so,addr = tcp_sever.accept()
        
        # 5. 调用传输函数
        p1 = multiprocessing.Process(target=tran_data,args=(new_so,))

        p1.start()
        new_so.close() # 进程间不共享资源，关闭主进程链接的now_so
    # 6. 关闭监听套接字
    tcp_sever.close()


if __name__ == '__main__':
    main()