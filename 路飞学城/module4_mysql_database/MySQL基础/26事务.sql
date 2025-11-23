#TCL
/*

Transaction Control Language 事物控制语言

事务:
一个或一组SQL语句组成一个执行单元,这个执行单元要么全部执行，要么全部不执行
案例: 转账
a 1000
b 1000

update 表 set a的余额=500 where name = 'a';
意外
update 表 set b的余额=500 where name = 'b';

事务的特性：ACID
原子性：一个事务不可再分割，要么都执行要么都不执行
一致性：一个事务执行会使数据从一个一致状态切换到另一个一致状态
隔离性: 一个事务的执行不受其他事务的干扰
持久性: 一个事务一旦提交，则会永久的改变数据库的数据


事务的创建
隐式事务:事务没有明显的开启和结束的标记
	 比如insert update delete语句

显式事务:事务具有明显的开启和结束的标记 前提是:必须先设置自动提交功能禁用

set autocommit=0; 禁用

语法：  1.开启事务
	set autocommit=0; 禁用
	start transation;可选的
	2.编写事务中的SQL语句(select insert update delete增删改查)
	语句1;
	语句2;
	....
	3.结束事务
		方式1：commit;提交事务
		方式2；rollback;回滚事务
		
		
事务的隔离级别： 
	read uncommitted:出现脏读、幻读、不可重复读
	read committed:避免脏读，出现幻读、不可重复读  (Oracle默认)
	repeatable read: 避免脏读、幻读，出现不可重复读 (MySQL默认)
	serializable:都可避免
*/

SHOW ENGINES;显示MySQL的引擎

#演示事务的使用步骤

DROP TABLE IF EXISTS ACCOUNT;
CREATE TABLE ACCOUNT(
	id INT PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(20),
	balance DOUBLE
);
TRUNCATE TABLE ACCOUNT;
SET auto_increment_increment=1;
INSERT INTO ACCOUNT(username,balance) 
VALUES('zwj',1000),('zm',1000);
SELECT * FROM ACCOUNT;

#开启事务
SET autocommit = 0;
START TRANSACTION;
#编写一组事务的语句
UPDATE ACCOUNT SET balance = 500 WHERE username = 'zwj';
UPDATE ACCOUNT SET balance = 1500 WHERE username = 'ZM';
#结束事务-提交
COMMIT;

#开启事务
SET autocommit = 0;
START TRANSACTION;
#编写一组事务的语句
UPDATE ACCOUNT SET balance = 500 WHERE username = 'zwj';
UPDATE ACCOUNT SET balance = 1500 WHERE username = 'ZM';
#结束事务-回滚
ROLLBACK;



SELECT @@transaction_isolation;#查看当前隔离级别

SET SESSION TRANSACTION ISOLATION LEVEL 隔离级别;#设置隔离级别

SELECT * FROM ACCOUNT;
#演示设置保存点
SAVEPOINT 节点名;  #设置保存点 只能搭配rollback to xx使用

SET autocommit=0;
START TRANSACTION;
DELETE FROM ACCOUNT WHERE id=1;
DELETE FROM ACCOUNT WHERE id=2;
SAVEPOINT a;#设置保存点
DELETE FROM ACCOUNT WHERE id=5;
ROLLBACK TO a;#回滚到a这个保存点处

#2.delete和truncate在事务使用时的区别 

#①delete
SET autocommit=0;
START TRANSACTION;
DELETE FROM ACCOUNT;
ROLLBACK;

#②truncate
SET autocommit=0;
START TRANSACTION;
TRUNCATE TABLE ACCOUNT;
ROLLBACK;




