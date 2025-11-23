#DDL
/*

数据定义语言

库和表的管理(结构):
	一、库的管理: 创建、修改、删除
	二、表的管理: 创建、修改、删除
	
创建:create
修改:alter
删除:drop
	
*/


#一、库的管理
#1.库的创建
/*
语法:
	create database [if not exists] 库名;
*/

#创建库Books
CREATE DATABASE IF NOT EXISTS Books;

USE books;
#2.库的修改 (库名没法改)
	#可以更改库的字符集
	ALTER DATABASE books CHARACTER SET gbk;

#3.库的删除
DROP DATABASE IF EXISTS books;





#二、表的管理
#1.表的创建
/*

语法:
	create table 表名（
		列名 列的类型[(长度) 约束],
		列名 列的类型[(长度) 约束],
		.......
		列名 列的类型[(长度) 约束]
	
	）

*/


#创建book表
CREATE TABLE book(
	id INT, #编号
	bName VARCHAR(20), #图书名
	price DOUBLE, #价格
	authorId INT, #作者编号
	publishDate DATETIME #出版日期
	
);

 DESC book;

#创建author表
CREATE TABLE author(
	id INT,
	au_name VARCHAR(20),
	nation VARCHAR(10)
);
 DESC author;



#2.表的修改
/*
语法:
	alter table 表名 add|drop|change|modify column 列名 [列类型 约束];
	alter table 表名 rename to 新表名;


*/
#①.修改列名
ALTER TABLE book CHANGE COLUMN publishDate pubDate DATETIME;

#②.修改列的类型或约束
ALTER TABLE book MODIFY COLUMN pubDate TIMESTAMP;

#③.添加新列
ALTER TABLE author ADD COLUMN annual DOUBLE;

#④.删除列
ALTER TABLE author DROP COLUMN annual;

#⑤.修改表名
ALTER TABLE author RENAME TO book_author;

DESC book_author;



#3.表的删除
# drop table 表名;
DROP TABLE IF EXISTS `book_author`;

SHOW TABLES; #查看当前库的所有表


#通用的写法:

DROP DATABASE IF EXISTS 旧库名;
CREATE DATABASE 新库名;

DROP TABLES IF EXISTS 旧表名;
CREATE TABLES 新表名();



#4.表的复制
INSERT INTO author
VALUES(1,'村上春树','日本'),
(2,'林徽因','中国'),
(3,'雨果','法国'),
(4,'大仲马','法国');

#①.仅仅复制表的结构
CREATE TABLE copy 
LIKE author; #没数据

#②.复制表的结构+数据
CREATE TABLE copy2
SELECT * FROM author;

SELECT * FROM copy2;

#③.只复制部分数据
CREATE TABLE copy3
SELECT id,au_name 
FROM author 
WHERE nation = '法国';

SELECT * FROM copy3;

#④.仅仅复制某些字段(不包含数据) 直接设置一个恒不成立的筛选条件
CREATE TABLE copy4
SELECT id,au_name 
FROM author
WHERE 0;

SELECT * FROM copy4;














