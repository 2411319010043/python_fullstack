一、常见命令
1.查看当前所有的数据库
show databases;
2.打开指定的库
use 库名;
3.查看当前库的所有表
show tables;
4.查看其他库的所有表
show tables from 库名;
5.创建表
create table 表名(列名 列类型,
                列名 列类型);   
6.查看表结构
desc 表名;
7.查看服务器版本
    方式1：登录到MySQL服务器
    select version();
    方式2：没有登录到MySQL服务器
    mysql --version
    mysql --V