import socket

def main():
    # 创建一个udp套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # 绑定端口
    localaddr = ('',8080)
    udp_socket.bind(localaddr)
    # 获取对方的IP/port
    dest_ip = input('请输入对方的IP：')
    dest_port = int(input('请输入对方的port：'))
    
    while True:
    
    # 从键盘获取数据
        send_data = input('请输入要发送的数据：')
        if send_data == 'exit':
            break
        #  可以使用套接字收发数据
        #  发送数据 ---sendto('发送的内容','元组形式的对方ip以及port')
        udp_socket.sendto(send_data.encode('utf-8'),(dest_ip,dest_port))
        recv_data = udp_socket.recvfrom(1024) # recv_data中存储的是一个元组('接收到的数据'，('发送方的IP'，发送方的端口))
        recv_msg = recv_data[0] # 接收的消息
        send_addr = recv_data[1] # 发送方信息
        print('%s:%s' %(send_addr,recv_msg.decode('utf-8')))
    #  关闭套接字
    udp_socket.close()

if __name__ == "__main__":
    main()







"""
1.先发送 再接收
2.发送输入你要发送的话 还有你要发送给谁--IP port
3.接收 拆解元组 分别是对方的话 还有对方的IP port

"""