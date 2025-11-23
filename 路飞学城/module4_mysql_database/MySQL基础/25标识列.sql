#标识列
/*
又称为自增长列
含义:可以不用手动的插入值，系统提供默认的序列值
特点:
	1.标识列必须和主键搭配吗？ 不一定，但要求是一个key
	2.一个表可以有几个标识列？ 至多一个
	3.标识列的类型 只能用于数值类型的列
	4.标识列可以设置步长和起始值
*/
#一、创建表时设置标识列
DROP TABLE IF EXISTS tab_identity;
CREATE TABLE tab_identity(
	id INT PRIMARY KEY ,#auto_increment,
	NAME VARCHAR(20),
	seat INT #char(1) unique auto_increment #报错
);
TRUNCATE TABLE tab_identity;#清空数据

INSERT INTO tab_identity(id,NAME)VALUES(NULL,'john');
INSERT INTO tab_identity(NAME)VALUES('lili');
SELECT * FROM tab_identity;

#查看auto_increment的相关的系统变量
SHOW VARIABLES LIKE '%auto_increment%';
#设置步长
SET auto_increment_increment=3;
#设置起始位置
ALTER TABLE tab_identity AUTO_INCREMENT = 9;
INSERT INTO tab_identity(NAME)VALUES('b');
INSERT INTO tab_identity(NAME)VALUES('c');


#二、修改表时设置标识列

ALTER TABLE tab_identity MODIFY COLUMN id INT AUTO_INCREMENT;
DESC tab_identity;

#三、修改表时删除标识列
ALTER TABLE tab_identity MODIFY COLUMN id INT ;





