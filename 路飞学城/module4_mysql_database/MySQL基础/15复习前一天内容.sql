#复习前一天内容
/*
一、SQL99语法
	1.内连接
	
		语法:select 查询列表
		     from 表1 别名
		     [inner] join 表2 别名 on 连接条件
		     where 筛选条件
		     group by 分组列表
		     having 分组后的筛选条件
		     order by 排序
		     limit 分页查询;
		     
		 特点:1.表的顺序不分主从表
		      2.内连接的结果 = 多表的交集部分
		      3.n表连接 至少需要n-1个连接条件
		     
		 分类:1.等值连接
		      2.非等值连接
		      3.自连接
		
		
		
		
	2.外连接
	
		语法:select 查询列表
		     from 表1 别名
		     left|rigt|full[outer] join 表2 别名 on 连接条件
		     where 筛选条件
		     group by 分组列表
		     having 分组后的筛选条件
		     order by 排序
		     limit 分页查询;
		     
		特点:1.查询的结果=主表中的所有的行，其中从表和它匹配的将显示匹配行，如果从表没有匹配的则显示null
		     2.主表 left join 从表 ，从表 right join 主表，full join 两边都是主表
		     3.一般用于查询:除交际部分外剩余不匹配的行
		     
		
		
		
		
	3.交叉连接
		
		语法:select 查询列表
		     from 表1 别名
		     cross join 表2 别名 
		     where 筛选条件
		     group by 分组列表
		     having 分组后的筛选条件
		     order by 排序
		     limit 分页查询;
		     
		特点:类似笛卡尔乘积


*/


/*
二、子查询

1.含义:嵌套在其他语句内部的select语句称为子查询或内查询
       外边的语句可以是insert、update、delete、select等

2.分类
	(1)按出现位置
	
		select后面
			标量子查询(单行子查询):结果集为一行一列

		from后面
			表子查询:结果集为多行多列

		where\having后面
			标量子查询(单行子查询):结果集为一行一列
			列子查询(多行子查询):结果集为多行一列
			行子查询:结果集为多行多列
			
		exists后面
			标量子查询(单行子查询):结果集为一行一列
			列子查询(多行子查询):结果集为多行一列
			行子查询:结果集为多行多列
			表子查询:结果集为多行多列
		
	(2)按子查询出现的结果集行列
	
		标量子查询(单行子查询):结果集为一行一列
		列子查询(多行子查询):结果集为多行一列
		行子查询:结果集为多行多列
		表子查询:结果集为多行多列
	
*/


#三、示例
#where或having后面
#1.标量子查询:查询最低工资的员工姓名和工资
	#①最低工资
SELECT MIN(salary) 
FROM `employees`;
	#②结合①查询员工姓名和工资
SELECT `last_name`,`salary` 
FROM `employees` 
WHERE salary = (SELECT MIN(salary) FROM `employees`);


#2.列子查询:查询所有是领导的员工姓名
	#①先查询所有员工的manager_id
SELECT DISTINCT `manager_id` FROM `employees`;
	#②查询姓名,employee_id属于①
SELECT last_name FROM `employees` WHERE `employee_id` IN (SELECT `manager_id` FROM `employees`);




/*
四、分页查询
	1.应用场景:当查询的条目数太多，一页显示不全
	
	2.语法:
		select 查询列表
		from 表名
		......
		limit [offset],size;
		
	3.注意:
		offset代表的是起始的条目索引,默认从0开始
		size代表的是条目数
		
	4.公式:
		想显示的页数为page，每一页条目数为20
		offset= (page-1)*size



*/















