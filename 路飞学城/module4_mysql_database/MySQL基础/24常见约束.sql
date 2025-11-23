#常见约束
/*

含义:一种限制，限制表中的数据，保证表内的数据的准确和可靠

分类:
	1.NOT NULL 非空约束
	2.DEFAULT 默认约束:用于保证该字段有默认值
	3.PRIMARY KEY 主键约束：保证字段的值具有唯一性且非空
	4.UNIQUE 唯一约束:保证字段的值具有唯一性，可以为空(可以有多个null)
	5.CHECK 检查约束[MySQL不支持]
	6.FOREIGN KEY 外键约束：用于限制两个表的关系，用于保证字段的值必须来自主表的关联列的值
			        在从表添加外键约束，用于引用主表中某列的值
			        
添加约束的时机:
	1.创建表时
	2.修改表时
约束的添加分类:
	列级约束
		六大约束语法上都支持，但外键约束没有效果
	表级约束
		除了非空、默认，其他都支持
		
		
主键和唯一的对比【面试】:
			保证唯一性	是否允许为空	一个表中可以有多少个约束	是否允许组合
	主键		     是		     否			至多有一个		 是但不推荐
	唯一 		     是		     是			可以有多个		 是但不推荐


外键特点：①.要求在从表上设置外键关系
	  ②.从表的外键列类型和主表的关联列的类型要一致或兼容
	  ③.主表的关联列必须是一个key(一般是主键、唯一键)
	  ④.插入数据时，先插入主表，再插入从表
	     删除数据时，先删除从表，在删除主表
*/

CREATE TABLE 表名(
	字段名 字段类型 列级约束,
	字段名 字段类型,
	表级约束
	);


#一、创建表时添加约束
#1.添加列级约束
/*
语法:
	直接在字段类型后面追加约束类型
*/
CREATE DATABASE students;
USE students;
CREATE TABLE stuinfo(
	id INT PRIMARY KEY, #主键
	stuName VARCHAR(20) NOT NULL,#非空
	gender CHAR(1)CHECK(gender='男' OR gender = '女'),#检查
	seat INT UNIQUE,#唯一
	age INT DEFAULT 18,#默认
	majorId INT REFERENCES major(id)#外键

);

CREATE TABLE major(
	id INT PRIMARY KEY,
	majorName VARCHAR(20)
);


DESC stuinfo;
SHOW INDEX FROM stuinfo; #查看表中所有的索引，包含主键、外键、唯一

#2.添加表级约束
/*
语法:在所有字段的最下边
 [constraint 约束名] 约束类型(字段名)


*/

DROP TABLE IF EXISTS stuinfo;

CREATE TABLE stuinfo(
	id INT ,
	stuName VARCHAR(20) ,
	gender CHAR(1),
	seat INT ,
	age INT ,
	majorId INT ,
	
	CONSTRAINT pk PRIMARY KEY (id),#主键
	CONSTRAINT uq UNIQUE(seat),#唯一键
	CONSTRAINT ck CHECK(gender = '男' OR gender = '女'),#检查
	CONSTRAINT fk_stuinfo_major FOREIGN KEY (majorId) REFERENCES major(id) #外键

);

SHOW INDEX FROM stuinfo; #查看表中所有的索引，包含主键、外键、唯一


#通用的写法

CREATE TABLE IF NOT EXISTS stuinfo(
	id INT PRIMARY KEY,
	stuname VARCHAR(20) NOT NULL,
	sex CHAR(1),
	age INT DEFAULT 18,
	seat INT UNIQUE,
	majorid INT,
	CONSTRAINT fk_stuinfo_major FOREIGN KEY (majorid) REFERENCES major(id)
);
#验证一个表中的字段age的unique约束是否可以同时有多个null
INSERT INTO major 
VALUES(1,'java'),
	(2,'h5');
SELECT * FROM major;
INSERT INTO stuinfo VALUES(1,'yy','女',18,NULL,1);
INSERT INTO stuinfo VALUES(2,'bb','女',17,1,1);
INSERT INTO stuinfo VALUES(3,'cc','女',11,NULL,2);
INSERT INTO stuinfo VALUES(4,'dd','女',NULL,23,2);
INSERT INTO stuinfo VALUES(5,'xx','女',NULL,11,2);
SELECT * FROM `stuinfo`;







DROP TABLE IF EXISTS stuinfo;
CREATE TABLE stuinfo(
	id INT ,
	stuName VARCHAR(20) ,
	gender CHAR(1),
	seat INT ,
	age INT ,
	majorId INT 
);
#二、修改表时添加约束


/*
1.添加列级约束
	alter table 表名 modify column 字段名 字段类型 新约束;
	
2.添加表级约束
	alter table 表名 add [constraint 约束名] 约束类型(字段名)[外键的引用];
*/


#1.添加非空约束
ALTER TABLE stuinfo MODIFY COLUMN stuname VARCHAR(20) NOT NULL;

DESC stuinfo;
#2.添加默认约束
ALTER TABLE stuinfo MODIFY COLUMN age INT DEFAULT 20;

#3.添加主键
①列级约束
ALTER TABLE stuinfo MODIFY COLUMN id INT PRIMARY KEY;
②表级约束
ALTER TABLE stuinfo ADD PRIMARY KEY(id);

#4.添加唯一键
ALTER TABLE stuinfo MODIFY COLUMN seat INT UNIQUE;
ALTER TABLE stuinfo ADD UNIQUE(seat);

#5.添加外键
ALTER TABLE stuinfo ADD CONSTRAINT fk_stuinfo_major FOREIGN KEY(majorId) REFERENCES major(id);




#三、修改表时删除约束
#1.删除非空约束
ALTER TABLE stuinfo MODIFY COLUMN stuname VARCHAR(20) NULL;

DESC stuinfo;
#2.删除默认约束
ALTER TABLE stuinfo MODIFY COLUMN age INT NULL;

#3.删除主键
①列级约束
ALTER TABLE stuinfo MODIFY COLUMN id INT NULL;

②表级约束
ALTER TABLE stuinfo DROP PRIMARY KEY;

#4.删除唯一键
ALTER TABLE stuinfo MODIFY COLUMN seat INT NULL;
ALTER TABLE stuinfo DROP INDEX seat;

#5.删除外键
ALTER TABLE stuinfo DROP FOREIGN KEY fk_stuinfo_major;



#案例讲解
#1.向表 emp2 的 id 列中添加 PRIMARYKEY约束（my_emp_id_pk)
#列级约束不支持起名字
ALTER TABLE emp2 MODIFY COLUMN id INT PRIMARY KEY;
#表级约束
ALTER TABLE emp2 CONSTRAINT my_emp_id_pk ADD PRIMARY KEY(id);

#2.向表dept2 的 id列中添加 PRIMARYKEY约束（my_dept_id_pk)
ALTER TABLE dept2 CONSTRAINT my_dept_id_pk ADD PRIMARY KEY(id);

#3.向表emp2中添加列dept_id，并在其中定义FOREIGNKEY约束，与之相关联的列是dept2表中的id列。
ALTER TABLE emp2 ADD COLUMN dept_id INT;
ALTER TABLE emp2 CONSTRAINT fk_emp2_dept2 FOREIGN KEY(dept_id) REFERENCES dept2(id);


#列级约束、表级约束对比       	  位置		支持的约束类型	 	 	是否可以起约束名
	列级约束		列的后面	语法都支持 外键无效果		不可以
	表级约束		所有列的下面	默认和非空不支持		可以(主键无效果)





