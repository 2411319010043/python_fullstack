#测试题
#1、创建表Book表，字段如下：
/*bid整型.要求主键.
bname字符型，要求设置唯一键，并非空
price 浮点型‘要求有默认值 10
btypeId类型编号，要求引『用bookType表的id字段
已知bookType表（不用创建），字段如下。
id
name
*/
CREATE TABLE Book(
	bid INT PRIMARY KEY,
	bname VARCHAR(20) UNIQUE NOT NULL,
	price FLOAT DEFAULT 10,
	btypeId INT,
	
	CONSTRAINT FOREIGN KEY (bTypeid) REFERENCES bookType(id) #外键
);

/*2.开启事务
向表中插入1行数据，并结束*/
#开启事务
SET autocommit = 0;
START TRANSACTION;

INSERT INTO Book VALUES(
	1,'爱的教育',111.1,1
);
#结束事务-提交
COMMIT;

/*3、创建视图，实现查询价格大于100的书名和类型名*/
CREATE VIEW myv1
AS 
SELECT bname, NAME ,price 
FROM Book b1 
JOIN bookType2 ON b1.btypeId = b2.id;

SELECT bname,NAME 
FROM myv1,Book 
WHERE price > 100;

/*4、修改视图，实现查询价格在90-120之间的书名和价格*/
CREATE OR REPLACE VIEW myv1
AS SELECT bname,price FROM Book;
 
SELECT * FROM myv1 WHERE price >90 AND price < 120;


/*5、删除刚才建的视图*/

DROP VIEW myv1;

