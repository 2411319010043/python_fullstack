#二、SQL99语法
/*
语法:
	select 查询列表
	from 表1 别名1 [连接类型]
	join 表2 别名2 
	on 连接条件
	where 筛选条件
	group by 分组列表
	having 分组后的筛选
	order by 排序列表
分类:	
	内连接 inner
	外连接 
		左外 left[outer]
		右外 right[outer]
		全外 full [outer]
	交叉连接 cross

*/

#一、内连接
/*
语法:
	select 查询列表
	from 表1 别名1 inner
	join 表2 别名2 
	on 连接条件
	where 筛选条件
	group by 分组列表
	having 分组后的筛选
	order by 排序列表;
	
分类:
	等值连接
	非等值连接
	自连接
特点:
	1.添加排序、分组、筛选
	2.inner可以省略
	3.筛选条件放在where后面 连接条件放在on后面，提高阅读性
	4.SQL99和SQL92的等值连接效果一样
*/

#等值连接
#1，查询员工名、部门名（调换位置）
SELECT last_name,department_name
FROM employees e INNER
JOIN departments d
ON e.`department_id` = d.`department_id`;

#2.查询名字中包含e的员工名和工种名（筛选）
SELECT last_name,job_title
FROM employees e INNER
JOIN jobs j 
ON e.`job_id` = j.`job_id`
WHERE last_name LIKE '%e%' AND `job_title` LIKE '%e%';

#3.查询部门个数》3的城市名名和部门个数，（分组+筛选）
SELECT COUNT(*) 个数,city
FROM locations l INNER
JOIN departments d
ON d.`location_id` = l.`location_id`
GROUP BY city
HAVING 个数>3;

#4.查询哪个部门的部门员工个数》3的部门名和员工个数，并按个数降序（排序）
SELECT `department_name`,COUNT(*)
FROM `employees` e INNER
JOIN `departments` d ON d.`department_id` = e.`department_id`
GROUP BY `department_name`
HAVING COUNT(*) >3
ORDER BY COUNT(*) DESC;

#5.查询员工名、部门名、工种名，并按部门名降序
SELECT `last_name`,`department_name`,`job_title`
FROM employees e INNER
JOIN `departments` d ON e.`department_id` = d.`department_id`
JOIN `jobs` j ON j.`job_id` = e.`job_id`
ORDER BY `department_name` DESC;



#非等值连接
#查询员工的工资级别

SELECT salary,grade_level
FROM `employees` e INNER
JOIN `job_grades` j 
ON salary BETWEEN `lowest_sal` AND `highest_sal`;

#查询每个工资级别的个数 >2，并且降序
SELECT COUNT(*) AS 个数 ,`grade_level` 工资等级
FROM `employees` e 
JOIN `job_grades` j ON salary BETWEEN `lowest_sal` AND `highest_sal`
GROUP BY 工资等级
HAVING 个数 > 20
ORDER BY 工资等级 DESC;

#自连接
#查询员工名和上级的名字 姓名中包含字符k的
SELECT e.`last_name`,m.`last_name`
FROM `employees` e
JOIN `employees` m ON e.`manager_id` = m.`employee_id`
WHERE e.last_name LIKE '%k%';


#二、外连接
/*
应用场景:用于查询一个表中有,另一个表中没有的记录
	
特点:
	1.外连接的查询结果为主表中的所有记录
		如果从表中有相匹配的值，则显示匹配的值
		如果从表中没有相匹配的值，则显示null
		外连接查询结果 = 内连接结果 + 主表中有而从表没有的记录
	2.左外连接，left 左边的是主表
	  右外连接，right join 右边的是主表
	3.左外和右外交换两个表的顺序，可以实现同样的效果
	4.全外连接 = 内连接的结果+表1中但表2中没有的+表2中但表1中没有的
*/
#引入:查询没有男朋友的女神名 boys不在1-4之间的 (查询男朋友 不在男神表的女神名)
SELECT * FROM beauty;
SELECT * FROM boys;

#左外连接
SELECT b.name,bo.*
FROM `beauty` b
LEFT OUTER JOIN boys bo
ON b.`boyfriend_id` = bo.`id`
WHERE bo.id IS NULL;

#右外连接
SELECT b.name,bo.*
FROM boys bo
RIGHT OUTER JOIN `beauty` b
ON b.`boyfriend_id` = bo.`id`
WHERE bo.id IS NULL;

#案例
#查询哪个部门没有员工
USE `myemployees`;
SELECT * FROM `departments`;
SELECT * FROM `employees`;

SELECT d.`department_name` AS 部门名称 ,e.`employee_id` AS 员工id
FROM `departments` d
LEFT OUTER JOIN `employees` e
ON d.`department_id` = e.`department_id`
WHERE e.`department_id`IS NULL;

#查询哪个员工的部门id为null
SELECT d.*,e.`employee_id`
FROM `departments` d
LEFT OUTER JOIN `employees` e
ON d.`department_id` = e.`department_id`
WHERE e.`employee_id`IS NULL;

#全外连接 (mysql不支持)
USE girls;
SELECT b.*,bo.*
FROM beauty b
FULL OUTER JOIN boys bo
ON b.`boyfriend_id` = bo.`id`;

#交叉连接 #99语法中的笛卡尔乘积
SELECT b.*,bo.*
FROM beauty b
CROSS JOIN boys bo;



#SQL92和SQL99
/*
功能:sql99支持的较多
可读性:sql99实现连接条件和筛选条件的分离，可读性较高
*/

#案例

#一、查询编号>3的女神的男朋友信息，如果有则列出详细，如果没有，用NULL填充

USE girls;
SELECT b.id 女神id ,bo.* 
FROM beauty b
LEFT OUTER JOIN boys bo
ON bo.id = b.`boyfriend_id`
WHERE b.id > 3;


#二、查询哪个城市没有部门

USE `myemployees`;
SELECT city,`department_name`
FROM locations l
LEFT OUTER JOIN `departments` d
ON l.location_id = d.location_id
WHERE department_name IS NULL;


#三、查询部门名为SAL工或IT的员工信息

SELECT `department_name`,e.*
FROM `departments` d
LEFT OUTER JOIN `employees` e
ON e.`department_id` = d.`department_id`
WHERE `department_name` IN ('SAL','IT');


