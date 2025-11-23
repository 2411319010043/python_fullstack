'''
流程：1.用户输入路径
     2.然后我们进到文件夹中统计有多少个文件
     3.然后我们循环复制文件到新的文件夹
'''
from multiprocessing import Pool
import os


def copy_file(file_name,old_FileName,new_FileName):
    '''完成文件copy'''
    print('------模拟copy文件：从%s----->%s 文件名是：%s' % (old_FileName,new_FileName,file_name))
    old_f = open(old_FileName + '/' + file_name, 'rb')
    content = old_f.read()
    old_f.close()

    new_f = open(new_FileName + '/' + file_name,'wb')
    new_f.write(content)
    new_f.close()


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
    
    # 5. 向进程池中添加 copy文件的任务
    for file_name in file_names:
        p.apply_async(copy_file,args= (file_name,old_FileName,new_FileName))  #要把 要复制的文件夹 从哪来的 到哪去 都要传过去
 
    
    

    p.close()
    p.join()


if __name__ == '__main__':
    main()
















