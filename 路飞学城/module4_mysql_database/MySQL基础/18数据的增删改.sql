#DML语言
/*
数据操作语言
插入 insert
修改 update
删除 delete
*/

#一、插入语句
#1.方式一:
/*
语法:
	insert into 表名(列名,...)
	values(值1,....)
*/

USE girls;

#1.插入的值类型要与列的类型一致或兼容
INSERT INTO beauty(id,NAME,sex,`borndate`,`phone`,`photo`,`boyfriend_id`)
VALUES(13,'唐艺昕','女','1990-4-23','189888888',NULL,2);

SELECT * FROM `beauty`;

#2.可以为null的列是如何插入值的？
#方式一：
INSERT INTO beauty(id,NAME,sex,`borndate`,`phone`,`photo`,`boyfriend_id`)
VALUES(13,'唐艺昕','女','1990-4-23','189888888',NULL,2);
#方式二：
INSERT INTO beauty(id,NAME,sex,`borndate`,`phone`,`boyfriend_id`)
VALUES(14,'古力娜扎','女','1990-4-23','138000000',9);

#3.列的顺序是否可以调换
INSERT INTO beauty(NAME,sex,id,phone)
VALUES('倪妮','女',15,'18000000');

#4.列数和值的个数必须一致,不一致就报错
INSERT INTO beauty(NAME,sex,id,phone,`boyfriend_id`)
VALUES('关晓彤','女',16,'18000000');

#5.可以省略列名,默认所有列,且列的顺序和表中列的顺序要一致
INSERT INTO beauty
VALUES(18,'林允','女','1998-5-5','15599999',NULL,NULL);




#方式二:
/*
语法:
	insert into 表名
	set 列名=值，列名=值....
*/

INSERT INTO beauty
SET id=16,NAME='鞠婧祎',phone='15544888888';


#两种方式对比

#1.方式一 支持插入多行
INSERT INTO beauty
VALUES(18,'林允','女','1998-5-5','15599999',NULL,NULL),
VALUES(18,'林允','女','1998-5-5','15599999',NULL,NULL);

#2.方式一 支持子查询
INSERT INTO beauty(id,NAME,phone)
SELECT 17,'宋茜','12255555';



#二、修改语句
/*


1.修改单表的记录
语法:
	update 表名
	set 列 = 值
	where 筛选条件;
	
	
2.修改多表的记录[补充]
sql92：
语法：
	update 表1 别名,表2 别名
	set 列=值
	where 连接条件
	and 筛选条件;
	
sql99:
语法：
	update 表1 别名
	inner|left|right join 表2 别名
	on 连接条件
	set 列=值
	where 筛选条件;
*/

SELECT * FROM `beauty`;

#1.修改单表的记录
#修改beauty表中姓唐的电话改成110

UPDATE beauty
SET phone = '110'
WHERE NAME LIKE "唐%";

SELECT * FROM `boys`;

#修改boyes表中id值为2的名称为张伟，魅力值10

UPDATE boys
SET boyName = '张飞',userCP = 10
WHERE id = 2;

#2.修改多表的记录

#修改张无忌的女朋友的手机号为114

UPDATE beauty b1,boys b2
SET b1.phone = '114'
WHERE b2.id = b1.`boyfriend_id`
AND b1.`boyfriend_id` = 1;

#修改没有男朋友的女神的男朋友编号都为张飞
UPDATE boys b2
RIGHT JOIN  beauty b1
ON b1.`boyfriend_id` = b2.id
SET b1.`boyfriend_id` = 2
WHERE b1.`boyfriend_id` IS NULL OR `boyfriend_id` > 4;

UPDATE boys b2
RIGHT JOIN  beauty b1
ON b1.`boyfriend_id` = b2.id
SET b1.`boyfriend_id` = 2
WHERE b2.id IS NULL;  #以beauty为主表，去找boys中没有对应id的记录。



#三、删除语句
/*

方式一: delete
语法: 
1.单表的删除
	delete from 表名
	where 筛选条件
2.多表的删除[补充]
	SQL92:
		delete 要删除表的别名
		from 表1 别名,表2 别名
		where 连接条件
		and 筛选条件;
	SQL99：
		delete 要删除表的别名
		from 表1 别名
		inner|left|right join 表2 别名 on 连接条件
		where 筛选条件;
		
方式二: truncate
语法: truncate table 表名；

*/

SELECT * FROM beauty;

#方式一: delete

#1.单表的删除
#删除手机号码最后一位为9的信息

DELETE FROM beauty
WHERE phone LIKE '%9';

#2.多表的删除
#删除张无忌的女朋友的信息
DELETE b1
FROM beauty b1 
LEFT JOIN boys b2 ON b1.`boyfriend_id` = b2.`id`
WHERE b2.boyName = '张无忌';

#删除杨颖以及男友的信息
DELETE b,bo
FROM beauty b
INNER JOIN boys bo ON b.`boyfriend_id` = bo.`id`
WHERE b.name = 'Angelababy';


#方式二:truncate

#把boys表清空

TRUNCATE TABLE boys ;



#delete 和 truncate 对比[面试]
/*

1.delete 可以加 where 条件
2.truncate 删除效率高
3.假如要删除的表中有自增长列，
	用delete删除后，再次插入数据，自增长列的值从断点开始，
	用truncate删除后，再次插入数据，自增长列的值从1开始
4.truncate 删除没有返回值，delete删除有返回值
5.truncate 删除不能回滚，delete删除可以回滚

*/

SELECT * FROM boys;

DELETE FROM boys;  #id最后为4
INSERT INTO boys (`boyName`,`userCP`)VALUES('曹操','200');   #id从5开始
INSERT INTO boys (`boyName`,`userCP`)VALUES('刘备','100');   
INSERT INTO boys (`boyName`,`userCP`)VALUES('关云长','150');   

TRUNCATE TABLE boys;
INSERT INTO boys (`boyName`,`userCP`)VALUES('曹操','200');   #id从1开始
INSERT INTO boys (`boyName`,`userCP`)VALUES('刘备','100');   
INSERT INTO boys (`boyName`,`userCP`)VALUES('关云长','150');   


















