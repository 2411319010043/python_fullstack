#复习前一天的内容
#一、事务
#1、事务：一条或多条SQL语句组成一个执行单位，一组SQL语句要么都执行要么都不执行
#2、事务的三种特性：
	#1.原子性:一个事务是不可再分割的整体，要么都执行要么都不执行
	#2.一致性:一个事务可以使数据从一个一致状态切换到另一个一致的状态
	#3.隔离性:一个事务不受其他事物的干扰，多个事务是相互隔离的
	#4.持久性:一个事务一旦提交了，则永久的持久化到本地
#3、事务的使用步骤
	#隐式事务:没有明显的开启和结束，本身就是一条事务可以自动提交，比如insert、update
	#显式事务:具有明显的开启和结束
	#使用显式事务:
	#1.开启事务
		SET autocommit = 0;
		START TRANSACTION;
	#2.编写一组SQL逻辑语句(仅支持 insert,update,delete,select)
		#[设置回滚点: savepoint 回滚点;] 
	#3.结束事务
		#提交：commit;
		#回滚: rollback;
		#[回滚到回滚点: rollback to 回滚点名;]
#4、并发事务
	#1.事务的并发问题是如何发生的？
		#多个事务 同时 操作 同一个数据库的相同数据时
	#2.并发问题都有哪些？
		#脏读:一个事务读取了其他事务还没有提交的数据
		#幻读:一个事务提取了其他事务还没有提交的数据，只是读到其他事务'插入'的数据
		#不可重复读:一个事务多次读取，结果不一样
	#3.如何解决并发问题?
		#通过设置隔离级别
	#4.隔离级别 			脏读	不可重复读	幻读
		# read uncommitted:读未提交	 √	    √             √
		# read committed:读已提交	 ×	    √             √
		# repeatable read:可重复读	 ×	    ×		  √    MySQL默认
		# serializable：串行化		 ×          ×             ×



#二、视图
	#1.含义:mysql5.1版本出现的新特性，是一个虚拟表 数据来自于表，执行时动态生成
		#优点： 简化了SQL语句
			#提高了SQL通用性
			#保护基表的数据，提高了安全性
	#2.创建:
		CREATE VIEW 视图名
		AS
		查询语句;
	#3.修改:
		方式一:
			CREATE OR REPLACE 视图名
			AS
			查询语句;
		方式二:
			ALTER VIEW 视图名
			AS
			查询语句;
	#4.删除:
		DROP VIEW 视图名;
	#5.查看:
		DESC 视图名;
		SHOW CREATE VIEW 视图名;
	#6.使用:
		#插入 insert
		#修改 update
		#删除 delete
		#查看 select
		#注:视图一般用于查询，而不是更新的，所以具备以下特点的视图不允许更新
			#1.包含分组函数 group by,distinct,having,union
			#2.join
			#3.常量视图
			#4.where后的子查询用到了from中的表
			#5.用到了不可更新的视图
	#7.视图和表的对比:
		关键字	是否占用物理空间		使用
	视图	VIEW	占用较小，只保存SQL逻辑		一般用于查询
	表	TABLE	保存实际的数据			增删改查



#三、约束
#1.约束分类
NOT NULL:非空，该字段的值必填
PRIMARY KEY:主键，该字段的值不可重复且非空
UNIQUE:唯一，该字段的值不可重复
DEFAULT:默认值
CHECK:检查 MySQL不支持
FOREIGN KEY:外键，该字段的值引用了另外表的字段

	#1.主键和唯一的区别
		/*主键不可重复且非空
		唯一键不可重复但可以有一个null值 
		主键一个表中只能有一个
		唯一键一个表中可以有多个
		*/

	#2.外键
		#1.用于限制两个表的关系，从表的字段值引用了主表的某字段值
		#2.外键列和主表的被引用列要求类型一致，意义一样，名称无要求
		#3.主表的被引用列要求时一个key
		#4.插入数据，先插入主表
		  #删除数据，先删除从表 可以通过以下两种方式 删除主表的记录

			USE students;

			SHOW INDEX FROM major;
			SHOW INDEX FROM stuinfo;
			ALTER TABLE stuinfo DROP FOREIGN KEY fk_stu_major;
			#传统的方式添加外键
			ALTER TABLE stuinfo ADD CONSTRAINT fk_stu_major FOREIGN KEY (majorid) REFERENCES major(id);

			SELECT * FROM major;
			DESC major;
			#添加专业
			INSERT INTO major VALUES(3,'python'),(4,'c'),(5,'vb');

			SELECT * FROM stuinfo;
			INSERT INTO stuinfo 
			VALUES(1,'john1','女',1,18,1),
				(2,'john2','女',2,18,2),
				(3,'john3','女',3,18,3),
				(4,'john4','女',4,18,4),
				(5,'john5','女',5,18,5),
				(6,'john6','女',6,18,1),
				(7,'john7','女',7,18,2);

			#直接删除专业表为3号的学生信息
			DELETE FROM major WHERE id=3;  #要想删除必须先删除从表的信息 这是因为外键约束在起作用
			#若想直接删除：
			#方式一：级联删除
			ALTER TABLE stuinfo 
			ADD CONSTRAINT fk_stu_major 
			FOREIGN KEY (majorid) REFERENCES major(id) ON DELETE CASCADE;
			#然后再删除
			DELETE FROM major WHERE id=3;  #成功了 主表和从表关于专业3的信息都被删除了

			#方式二:级联置空 将主表的信息删除，从表相关信息改为null
			ALTER TABLE stuinfo 
			ADD CONSTRAINT fk_stu_major 
			FOREIGN KEY (majorid) REFERENCES major(id) ON DELETE SET NULL;
			#然后再删除
			DELETE FROM major WHERE id=2;  #成功了 主表信息被删除了 从表改为null

#2.创建表时添加约束
CREATE TABLE 表名(
	字段名 字段类型 NOT NULL,
	字段名 字段类型 PRIMARY KEY,
	字段名 字段类型 UNIQUE,
	字段名 字段类型 DEFAULT 默认值,
	#表级约束
	CONSTRAINT 给约束规则起别名 FOREIGN KEY (从表字段名) REFERENCES 主表名(字段名)
	);

	#注意:		支持类型	可以起约束名
	#列级约束	除了外键	不可以
	#表级约束	除了默认和非空	 可以但对主键无效



#3.修改表时添加或删除约束
#①非空
	#添加
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型 NOT NULL;
	#删除
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型;
#②默认
	#添加
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型 DEFAULT 默认值;
	#删除
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型;
#③主键
	#添加列级约束
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型 PRIMARY KEY;
	#添加表级约束
ALTER TABLE 表名 ADD PRIMARY KEY(字段名);
	#删除列级约束
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型;
	#删除表级约束
ALTER TABLE 表名 DROP PRIMARY KEY;
#④唯一
	#添加列级约束
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型 UNIQUE;
	#添加表级约束
ALTER TABLE 表名 ADD UNIQUE(字段名);
	#删除列级约束
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型;
	#删除表级约束
ALTER TABLE 表名 DROP INDEX 字段名;
#⑤外键
	#添加表级约束
ALTER TABLE 表名 ADD CONSTRAINT 给约束规则起的名 FOREIGN KEY 从表字段名 REFERENCES 主表名(字段名);
	#删除表级约束
ALTER TABLE 表名 DROP FOREIGN KEY 给约束规则起的名;


#四、自增长列


#1.特点：
	#①不用手动插入值，可以自动增长，默认从1开始，步长1
		#查看auto_increment的相关的系统变量
		SHOW VARIABLES LIKE '%auto_increment%';
		#设置步长
		SET auto_increment_increment=3;
		#设置起始位置
		ALTER TABLE tab_identity AUTO_INCREMENT = 值;
	#②一个表至多有一个自增长列
	#③只能支持数值型
	#④自增长列必须是一个key
	
	
#2.语法
	#创建表时设置自增长列
CREATE TABLE 表名(
	字段名 字段类型 约束 AUTO_INCREMENT
);
	#修改表时设置自增长列
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型 约束 AUTO_INCREMENT;
	#删除自增长列
ALTER TABLE 表名 MODIFY COLUMN 字段名 字段类型 约束;
























