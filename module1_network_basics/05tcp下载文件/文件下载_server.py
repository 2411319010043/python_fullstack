import socket


def send_file_2_client(new_sever_socket):

    # 5. 接收客户端发来的文件名
    raw_data = new_sever_socket.recv(1024*1024)
    s_name = raw_data.decode('utf-8').strip()
    print(f"请求的文件: '{s_name}'")

   
    # 7. 若存在 读取文件并进行传输
    try:
        with open(s_name,'rb') as f:
            s_data = f.read()
            new_sever_socket.send(s_data)
        print(f'文件{s_name} 发送成功')
    except Exception as ret:
        print(f'文件{s_name} 不存在')

    

def main():
    # 1. 创建套接字
    s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 绑定地址
    s_socket.bind(('',8080))

    # 3. 设为监听状态
    s_socket.listen(128)
    while True:
        # 4. 创建新的套接字 等待客户端连接
        new_sever_socket,sever_addr = s_socket.accept()

        # 6. 调用传输函数
        send_file_2_client(new_sever_socket)

        # 7. 关闭套接字
        new_sever_socket.close()
    s_socket.close()

if __name__ == '__main__':
    main()