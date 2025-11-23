#进阶5:分组查询
/*
语法:
	select 分组函数,列(要求出现在group by的后面)
	from 表名
	[where 筛选条件]
	group by 分组的列表
	[order by 子句]
注意:
	查询的列表要求是分组函数和group by后出现的字段
	
特点:
	1.分组查询中的筛选条件分为两类 
			  数据源          位置               关键字
	分组前筛选	原始表           group by子句的前面  where
	分组后筛选	分组后的结果集   group by子句的后面  having
	(1)分组函数做条件 肯定放在having子句中
	(2)能用分组前筛选的,优先考虑分组前筛选
	2.group by子句 支持单个字段、多个字段分组(多个字段之间用逗号隔开没有顺序要求),表达式或函数
	3.也可以添加排序顺序(排序放在整个分组查询的最后)
*/
#1.案例
#查询每个部门的平均工资

SELECT AVG(salary),`department_id`
FROM employees
GROUP BY `department_id`;

#查询每个工种 的最高工资

select max(salary),job_id 
from employees 
group by job_id;

#查询每个位置上的部门个数

select count(*),`location_id` 
from `departments`
group by location_id;


#2.添加筛选条件

#查询邮箱中包含a字符的，每个部门的平均工资

select avg(salary) as 平均工资 ,`department_id` as 部门编号
from employees
where email like '%a%'
group by `department_id`;

#查询有奖金的每个领导手下员工的最高工资

select max(salary),`manager_id`
from employees
where `commission_pct` is not null
group by `manager_id`;


#3.添加复杂的筛选条件

#查询哪个部门的员工个数>2
#1.先查询每个部门的员工数
#2.根据1的结果进行筛选，查询哪个部门的员工个数>2

select * from employees;
select `department_id` as 部门编号,count(*) as 员工数量 #涉及到个数 就用count(*)
from employees
group by `department_id`;

#报错了: WHERE子句不能使用聚合函数

SELECT COUNT(`department_id`)as 员工数量 ,`department_id` as 部门编号
FROM employees
where COUNT(`department_id`) >2
GROUP BY `department_id`;

#只能用having having筛选的条件列 必须出现在select后面

SELECT COUNT(`department_id`)AS 员工数量 ,`department_id` AS 部门编号
FROM employees
GROUP BY `department_id`
having COUNT(`department_id`) > 2;

#查询每个工种有奖金的员工的最高工资 >12000的工种编号和最高工资

select max(salary) as 最高工资 ,`job_id` as 工种编号
from employees
where `commission_pct` IS NOT NULL 
group by job_id
having 最高工资>12000;

#查询领导编号>102的每个领导手下的最低工资>5000的领导编号是哪个，以及其最低工资

select MIN(salary) AS 最低工资,`manager_id` as 领导编号
from employees
where `manager_id` > 102
group by `manager_id`
having 最低工资> 5000;


#4.按表达式或函数分组

#案例
#按员工姓名的长度分组，查询每一组的员工个数,筛选员工个数>5的有哪些

select COUNT(*) as 个数 ,LENGTH(concat(last_name,`first_name`)) as 长度
from employees
group by 长度
having 个数 >5;


#5.按多个字段分组

#案例: 查询每个部门每个工种的员工的平均工资

select avg(salary)as 平均工资,`department_id`as 部门,`job_id` as 工种
from employees
group by `department_id`,`job_id`;


#6.添加排序

#案例:
#查询每个部门每个工种的员工的平均工资,按照评价工资的高低显示

SELECT AVG(salary)AS 平均工资,`department_id`AS 部门,`job_id` AS 工种
FROM employees
GROUP BY `department_id`,`job_id` 
order by 平均工资 desc;



#案例讲解

#1.查询各job_id的员工工资的最大值、最小值、平均值、总和，并按job_id升序

select max(salary) as 最大值 ,min(salary) 最小值 ,avg(salary) 平均值 ,sum(salary) 总和,count(*),job_id
from employees
group by job_id
order by job_id asc;

#2.查询员工最高工资和最低工资的差距（DIFFERENCE)

select max(salary) - min(salary) as difference from employees;

#3.查询各个管理者手下员工的最低工资，其中最低工资不能低于6000，没有管理者的员工不计算在内

select min(salary) 最低工资,manager_id
from employees
group by manager_id
having 最低工资 >= 6000 and manager_id is not null;

#4.查询所有部门的编号，员工数量和工资平均值，并按平均工资降序

select COUNT(*) 员工数量 ,AVG(salary) 平均值 ,`department_id` 部门id
from employees
group by `department_id`
order by 平均值 desc;

#5.选择具有各个job_id的员工人数

select count(*),job_id
from employees
group by job_id
order by count(*) asc;



