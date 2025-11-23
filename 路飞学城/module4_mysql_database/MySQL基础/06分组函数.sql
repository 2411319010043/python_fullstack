#04进阶:二、分组函数
/*
功能:做统计使用,又称为统计函数 聚合函数
分类:
	sum 求和 avg 平均值 max 最大值 min 最小值 count 计算个数
特点:
	1.sum、avg一般只处理数值型
	  max、min、count可以处理任何类型
	2.分组函数忽略null值
	3.可以和distinct搭配使用
	4.count函数
	5.和分组函数一同查询的字段要求是group by后的字段
*/

#1.简单使用
SELECT SUM(salary) FROM employees;
SELECT AVG(salary) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT MIN(salary) FROM employees;
SELECT COUNT(salary) FROM employees;

#2.参数支持哪些类型
SELECT SUM(last_name),AVG(last_name)FROM employees;
SELECT SUM(hiredate),AVG(hiredate) FROM employees;
SELECT MAX(last_name),MIN(last_name) FROM employees;
SELECT MAX(hiredate),MIN(hiredate) FROM employees;
SELECT COUNT(`commission_pct`) FROM employees; #计算不为null的值
SELECT COUNT(last_name) FROM employees;

#3.是否忽略null值
SELECT SUM(`commission_pct`),AVG(`commission_pct`)FROM employees; #忽略
SELECT MAX(`commission_pct`),MIN(`commission_pct`) FROM employees;#忽略

#4.和distinct搭配 去重之后在.....
SELECT SUM(DISTINCT salary),SUM(salary) FROM employees;

#5.count函数的详细介绍
SELECT COUNT(salary) FROM employees;
SELECT COUNT(*) FROM employees;#查询表行数
SELECT COUNT(1) FROM employees;#统计都出来的一列1 这一列都是1  统计1的个数 相当于统计行数

#6.和分组函数一同查询的字段有限制
SELECT AVG(salary),`employee_id` FROM employees;

#案例讲解
#1.套询公司员工工资的最大值，最小值，平均值，总和
SELECT MAX(salary),MIN(salary),AVG(salary),SUM(salary) FROM employees;
#2.查询员工表中的最大入职时间和最小入职时间的相差天数（DIFFRENCE）
SELECT DATEDIFF(MAX(`hiredate`) , MIN(`hiredate`)) AS 相差天数 FROM employees;

SELECT DATEDIFF('2025-9-26' ,'2001-8-23');#求相差天数函数
#3.查询部门编号为90的员工个数
SELECT SUM(`department_id` = 90) FROM employees;
SELECT COUNT(*) FROM employees WHERE `department_id` = 90;