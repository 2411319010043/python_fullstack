import socket

def main():
    #1.创建套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   
    #2.绑定本地信息
    localaddr = ('',8080)
    udp_socket.bind(localaddr)
    while True:
        #从键盘获取数据
        send_data = input('请输入要发送的数据：')
        if send_data == 'exit':
            break
        #发送数据 ---sendto('发送的内容','元组形式的对方ip以及port')
        udp_socket.sendto(send_data.encode('gbk'),('127.0.0.1',8080))

        #3.接收数据
        recv_data = udp_socket.recvfrom(1024) #recv_data中存储的是一个元组('接收到的数据'，('发送方的IP'，发送方的端口))
        recv_msg = recv_data[0] #接收的消息
        send_addr = recv_data[1] #发送方信息
        
        #4.打印接收到的数据
        print('%s:%s'%(str(send_addr),recv_msg.decode('gbk'))) #发过来的时候是加码  现在读取要解码

    #关闭套接字
    udp_socket.close()



if __name__ == '__main__':
    main()









    