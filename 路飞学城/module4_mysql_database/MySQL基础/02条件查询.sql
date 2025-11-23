#进阶2：条件查询
/*
语法：
	select 
		查询列表
	from
		表名
	where 
		筛选条件;
分类:
	1.按条件表达式筛选
		条件运算符: > < = <>  <= >= 
	2.按逻辑表达式筛选
		逻辑运算符: and or not
	3.模糊查询
		like 
		between and 
		in 
		is null
*/
#1.按条件表达式筛选
#案例: 
#查询工资>12000的员工信息
SELECT * FROM employees WHERE salary > 12000;
#查询部门编号不等于90号的员工名和部门编号
SELECT 
	`last_name`,`first_name`,`department_id` 
FROM 
	employees 
WHERE 
	`department_id` <> 90;
	
#2.按逻辑表达式筛选
#案例：
#工资在10000到20000之间的员工名、工资以及奖金
SELECT `last_name`,`first_name`,`salary`,`commission_pct`
FROM employees 
WHERE salary > 10000 AND salary < 20000;

#查询部门编号不是在90-110之间的或者工资高于15000的员工信息
SELECT 
	* 
FROM 
	employees 
WHERE 
	(`department_id` < 90 OR `department_id` > 110) OR salary > 15000;

SELECT 
	* 
FROM 
	employees 
WHERE NOT 
	(`department_id` >= 90 AND `department_id` <= 110) OR salary > 15000;



#3.模糊查询
/*
like: 1.一般和通配符搭配使用 
	通配符：% 任意多个字符，包含0个字符
		——任意单个字符
between and
in 
is null / is not null
*/
#1.like
#案例:
#1.查询员工名中包含字符 a 的员工信息
SELECT * FROM employees WHERE `first_name` LIKE '%a%';
#2.查询员工名中第三个字符为e,第五个字符为a的员工名和工资
SELECT `last_name`,`first_name`,`salary` FROM employees WHERE `first_name` LIKE '__e_a%';
#3.查询员工名中第二个字符为_的员工名 使用转义字符\_
SELECT last_name,first_name FROM employees WHERE last_name LIKE '_\_%';
	#或者指定某个字符为转义字符
SELECT last_name,first_name FROM employees WHERE last_name LIKE '_$_%' ESCAPE '$';



#2. between and
/*
1.使用between and 可以提高语句的简洁度
2.包含临界值
3.两个临界值不要颠倒
*/
#案例:
#1.查询员工编号在100-120之间的员工信息
SELECT * FROM employees WHERE `employee_id` BETWEEN 100 AND 120;
 
#3.in
/*
  1.使用in提高语句简洁度
  2.不支持通配符
*/
#案例
#1.查询员工的工种名是 it_prog ad_vp ad_pres中的一个员工名和工种编号
SELECT 
	`last_name`,`first_name`,job_id 
FROM 
	employees WHERE job_id IN ('AD_PRES','AD_VP','IT_PROG');

#4.is null / is not null
#案例
#1.查询没有奖金的员工名和奖金率
SELECT last_name,`commission_pct` FROM employees WHERE commission_pct IS NULL;
#2.查询有奖金的员工名和奖金率
SELECT last_name,`commission_pct` FROM employees WHERE commission_pct IS NOT NULL;

#补充 安全等与 <=> 
#案例
#1.查询没有奖金的员工名和奖金率
SELECT last_name,`commission_pct` FROM employees WHERE commission_pct <=> NULL;
#2.查询工资为12000的员工信息
SELECT * FROM employees WHERE salary <=> 12000;

# is null <=>
#is null: 只可以判断null值，可读性较高，
#<=>: 可以判断null值 普通的数值 可读性较低










