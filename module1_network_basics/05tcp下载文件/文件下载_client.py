import socket

# 客户端
def main():
    # 1. 创建套接字
    c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2.获取服务器的IP，port
    s_ip = input('请输入连接服务器IP：')
    s_port = int(input('请输入连接服务器port：'))

    # 3. 连接服务器
    c_socket.connect((s_ip,s_port)) # 连接服务器

    # 4. 获取下载的文件名
    c_name = input('请输入要下载文件的名称：')

    # 5. 将名字发送到服务器
    c_socket.send(c_name.encode('utf-8'))

    # 6. 接收文件中的数据
    c_data = c_socket.recv(1024*1024)

    # 7. 保存接收到的数据到文件中
    if c_data:
        with open('[接收]'+c_name,'wb') as f:
            f.write(c_data)
    
    # 8. 关闭套接字
    c_socket.close()    


if __name__ == '__main__':
    main()




"""
1.建立连接--服务器 输入IP，port
2.发送下载文件的名称
3.开始接收数据
4.关闭套接字


"""




