#复习前一天的内容
#一、联合查询
#1.含义
	UNION #合并、联合，将多次查询结果合并成一个结果
#2.语法
	查询语句1
	UNION [ALL(去重)]
	查询语句2
	.....
#3.意义
	①.将一条复杂的语句拆分条多条简单语句
	②.适用于查询多个表的时候，查询的列基本一致
#4.特点
	①.要求多条查询语句的查询列数必须一致
	②.要求多条查询语句的查询的各列类型，顺序最好一致
	③.union自动去重 UNION ALL 解除去重
	
	
	
	
#总结语法:

SELECT 查询列表            7  
FROM 表名1 别名            1
连接类型 JOIN 表名2 别名   2
ON 连接条件                3
WHERE 筛选                 4
GROUP BY 分组列表          5
HAVING 分组后的筛选条件    6
ORDER BY 排序列表          8 
LIMIT 起始条目索引，条目数;9

#二、DML语言
#1.插入
	#①语法:
		INSERT INTO 表名[(字段名...)] VALUES(值),();
		INSERT INTO 表名 SET 字段名 = 值;
	#②特点: 要求值的类型和字段的类型要一致或兼容
		字段的个数和顺序不一定与原始表中的字段个数和顺序一致，但必须保证值和字段对应
		若表中有可以为null的字段，①字段和值都省略 ②字段写上，值用null
		字段名可以省略，默认所有列
	#③两种方式的区别:
		方式一支持一次性插入多行
		      支持子查询:INSERT INTO 表名 SELECT 查询列表 FROM 表名;
			

#2.修改
	#①修改单表的记录
		UPDATE 表名 SET 字段 = 值, 字段 = 值 [WHERE 筛选条件][LIMIT 条目数];
	#②修改多表的记录
		UPDATE 表名 别名 
		LEFT|RIGHT|INNER JOIN 表名 别名 
		ON 连接条件
		SET 字段 = 值, 字段 = 值 
		[WHERE 筛选条件];

#3.删除
	#① delete 
		#删除单表 delete from 表名 [where 筛选条件];
		#删除多表 delete 要删除的表别名 
		FROM 表名 别名 
		LEFT|RIGHT|INNER JOIN 表名 别名 
		ON 连接条件
		[WHERE 筛选条件];
	#② truncate
		TRUNCATE TABLE 表名;
	#③两种方式的对比[面试]
		1.delete删除后可以回滚，truncate不可以回滚
		delete可以多表删除 truncate只能单表删除
		2.truncate可以理解为清空 如果删除后再次插入标识列从1开始
		  delete删除后，如果再插入，标识列从断点开始
		3.delete可以添加筛选条件，truncate不可以添加筛选条件
		4.truncate效率比delete高
		5.truncate无返回值，delete有
		
		
		
		
#三、DDL语言
	#1.库的管理
		#①创建库  create database [if not exists] 库名 [character set 字符集名];
		#②修改库  
		#③删除库  drop database [if not exists] 库名;
	#2.表的管理
		#①创建表  create tables [if not exists] 表名(字段名 字段类型 [约束],.....);
		#②修改表  
			#添加列 alter table 表名 add column 列名 类型 [约束] [first|after 字段名];
			#修改列的类型/约束 alter table 表名 modify column 列名 新类型[新约束];
			#修改列名 alter table 表名 change column 旧列名 新列名 类型;
			#删除某个列 alter table 表名 drop column 列名;
			#修改表名 alter table 表名 rename [to] 新表名;
		#③删除表  
			DROP TABLE [IF EXISTS] 表名;

			
#四、复制表 可以跨库
	#1.复制表的结构
		CREATE TABLE 表名 LIKE 旧表;
	#2.复制表的结构+数据 
		CREATE TABLE 表名
		SELECT 查询列表 FROM 旧表 [WHERE 筛选];


#五、数据类型
	#1.数值型
		整型: TINYINT\SMALLINT\MEDIUMINT\INTEGER\BIGINT
			特点:①都可以设置有符号和无符合，默认有符号，通过unsigned设置无符号
			     ②查出范围会报错
			     ③有默认的长度是显示的最大宽度，若不够会用0在左边填充，必须搭配zerofill使用
		小数	定点 DEC\DECIMAL(M,D)
			浮点 FLOAT\DOUBLE(M,D)
				特点:①M和D： 可省略 但decimal省略的话 只能插入整数(10)部分 小数(0)部分插入不进去
						M 代表整数部分+小数部分的总长度 超过范围报错
						D 小数点保留D位 不够0填充
				     ②定点型的精度较高，如果要求插入数值精度较高如货币运算等可考虑使用
	#2.字符型
		CHAR\VARCHAR\BINARY\VARBINARY\ENUM\SET\TEXT\BLOB
		char：固定长度的字符，char(M)最大长度不超过M，可以省略 默认1
		VARCHAR:可变长度的字符，varchar(M) 最大长度不超过M，不可以省略
	#3.日期型
		DATE 保存日期
		TIME 保存时间
		YEAR 保存年
		DATETIME 保存日期+时间
		TIMESTAMP 保存日期+时间











		
		
		
		
		
		
