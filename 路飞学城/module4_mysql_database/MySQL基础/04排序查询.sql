#进阶3：排序查询
/*
引入：select * from employees;
语法：select 查询列表 from 表名 [where 筛选条件] order by 排序列表 [asc | desc];
特点: 1.asc代表升序(默认)，desc代表降序
      2.order by子句中可以支持 单个字段，多个字段，表达式，函数，别名
      3.order by子句一般放在查询语句的最后面,但limit子句除外
*/
#案例:
#1.查询员工信息，要求工资从高到低排序
SELECT * FROM employees ORDER BY salary DESC;
#2.查询部门编号大于等于90 的员工信息，按入职时间的先后排序[添加筛选条件]
SELECT * FROM employees WHERE `department_id` >= 90 ORDER BY `hiredate` ASC;
#3.按年薪的高低显示员工的信息和年薪[表达式排序]
SELECT 
	*,salary*12*(1+IFNULL(`commission_pct`,0)) AS 年薪 
FROM 
	employees 
ORDER BY 
	salary*12*(1+IFNULL(`commission_pct`,0)) DESC;
#4.按年薪的高低显示员工的信息和年薪[按别名排序]
SELECT 
	*,salary*12*(1+IFNULL(`commission_pct`,0)) AS 年薪 
FROM 
	employees 
ORDER BY 
	年薪 DESC;
#5.按姓名的长度显示员工的姓名和工资[按函数排序]
SELECT 
	`first_name`,`last_name`,`salary` 
FROM 
	employees 
ORDER BY 
	LENGTH(CONCAT(`last_name`,`first_name`)) ASC;
#6.查询员工信息，要求先按工资升序排序，再按员工编号降序排序[按多个字段排序]
SELECT * FROM employees ORDER BY salary ASC,`employee_id` DESC;

#案例讲解
#1.查询员工的姓名和部门号 年薪，按年薪降序 名字升序排序
SELECT 
	`last_name`,`first_name`,`department_id`, 12*salary*(1+IFNULL(`commission_pct`,0))AS 年薪 
FROM 
	employees 
ORDER BY 
	年薪 DESC,last_name ASC;
#2.选择工资不在8000到17000的员工的姓名和工资，按工资降序
SELECT 
	last_name,first_name,salary 
FROM 
	employees 
WHERE 
	salary NOT BETWEEN 8000 AND 17000 ORDER BY salary DESC;
#3.查询邮箱中包含e的员工信息，并先按邮箱的字节数降序，再按部门号升序
SELECT 
	* ,LENGTH(email) AS 邮箱字节数 
FROM 
	employees 
WHERE 
	email LIKE '%e%' ORDER BY LENGTH(email) DESC,`department_id` ASC;