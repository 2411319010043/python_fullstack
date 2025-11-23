'''
流程：1.用户输入路径
     2.然后我们进到文件夹中统计有多少个文件
     3.然后我们循环复制文件到新的文件夹
'''
from multiprocessing import Pool,Manager
import os


def copy_file(q,file_name,old_FileName,new_FileName):
    '''完成文件copy'''
    print('------模拟copy文件：从%s----->%s 文件名是：%s' % (old_FileName,new_FileName,file_name))
    old_f = open(old_FileName + '/' + file_name, 'rb')
    content = old_f.read()
    old_f.close()

    new_f = open(new_FileName + '/' + file_name,'wb')
    new_f.write(content)
    new_f.close()

    #如果拷贝完文件，就向队列中写入一个消息，表示已经完成
    q.put(file_name)

def main():
    # 1. 获取用户要copy的文件夹名称
    old_FileName = input('请输入要复制文件夹的名称：')

    # 2. 创建新的文件夹
    try:
        new_FileName = old_FileName + '[附件]'
        os.mkdir(new_FileName)
    except:
        pass

    # 3. 获取文件夹中所有待copy的文件名   os.listdir(文件夹名) 返回值是列表
    file_names = os.listdir(old_FileName)
    print('%s名下的文件：%s' %(old_FileName,file_names))

    # 4. 创建进程池
    p = Pool(10)
    
    # 5. 创建队列
    q = Manager().Queue

    # 6. 向进程池中添加 copy文件的任务
    for file_name in file_names:
        p.apply_async(copy_file,args= (q,file_name,old_FileName,new_FileName))  #要把 要复制的文件夹 从哪来的 到哪去 都要传过去
 
    
    

    p.close()
    all_file_num = len(file_names) # 所有的文件个数
    copy_ok_num = 0

    # 复制完一个文件 向队列中存放一个标志 主进程依次接收标志  属于进程间的通信 可以用队列实现
    while True:
        file_name = q.get()
        print('已经完成copy： %s' % file_name)
        
        copy_ok_num += 1
        print("\r拷贝的进度为： %.2f %%" % (copy_ok_num * 100 / all_file_num), end=" ")
        if copy_ok_num >= all_file_num:
            break

    print( )
if __name__ == '__main__':
    main()
















