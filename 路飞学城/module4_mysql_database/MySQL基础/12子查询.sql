#进阶7:子查询
/*
含义:出现在其他语句中的select语句,称为子查询或内查询
外部的查询语句，称为主查询或外查询

分类:
	按子查询出现的位置:
		select后面
			仅支持标量子查询
		from后面
			支持表子查询
		where或having后面
			支持标量子查询/列子查询/行子查询
		exists后面(相关子查询)
			支持表子查询
			
	按功能(结果集的行列数不同)分类:
		标量子查询(结果集只有一行一列)
		列子查询(结果集只有一列多行)
		行子查询(结果集只有多列多行/一行多列)
		表子查询(结果集一般为多行多列)
		
*/


#一、where或having后面
/*


特点:
	1.子查询放在小括号内
	2.子查询一般放在条件的右侧
	3.标量子查询，一般搭配单行操作符使用
	4.列子查询，一般搭配多行操作符使用 any/all
	5.子查询的执行优先于主查询执行，主查询的条件用到了子查询的结果
	
*/

#1.标量子查询(单行子查询)
#案例 谁的工资比Abel高

	#(1).查询abel的工资

SELECT salary 
FROM employees 
WHERE last_name IN ('Abel');

	#(2).比Abel工资高的工资是谁的

SELECT * 
FROM employees 
WHERE salary > (
		SELECT salary 
		FROM employees 
		WHERE last_name IN ('Abel')
);

#查询job_id与141号员工相同，salary比143号员工多的员工 姓名 job_id 和工资
	#(1)查询job_id 与141号相同的员工
SELECT job_id FROM employees WHERE `employee_id` = 141;
	#(2)查询salary比143号员工多的员工
SELECT last_name,job_id ,salary
FROM employees
WHERE salary > (
	SELECT salary 
	FROM employees 
	WHERE `employee_id` = 143
) AND job_id = (	
	SELECT job_id 
	FROM employees 
	WHERE `employee_id` = 141
);



#查询公司工资最少的员工的last_name,job_id和salary  
#先查员工信息 再去筛选 最低工资 的信息
	#1.查询公司的最低工资
	SELECT MIN(salary) FROM employees;
	#2.查询员工的last_name,job_id和salary  = 最低工资
SELECT last_name , job_id , salary 
FROM employees
GROUP BY salary,last_name,job_id
HAVING salary IN (SELECT MIN(salary) FROM employees);
#或
SELECT last_name,job_id,salary
FROM employees
WHERE salary = (SELECT MIN(salary) FROM employees);

#查询最低工资大于50号部门最低工资的部门id和其最低工资
	#1.50号部门的最低工资
SELECT MIN(salary) FROM employees WHERE department_id =50;
	#2.每个部门的最低工资
SELECT department_id ,MIN(salary) FROM employees GROUP BY department_id;

	#3.在2的基础上做筛选 满足min(salary) >1

SELECT department_id,MIN(salary) 
FROM employees 
GROUP BY department_id
HAVING 	MIN(salary)>(
	SELECT MIN(salary) 
	FROM employees 
	WHERE department_id =50
	);


#2.列子查询(多行子查询)

#题目：返回location id是1400或1700的部门中的所有员工姓名
SELECT last_name,location_id,department_name
FROM employees e ,departments d
WHERE e.`department_id` = d.`department_id` AND d.`location_id` IN(1400,1700);
	#利用子查询
	#1.查询location_id是1400或1700的部门编号
SELECT `department_id` 
FROM `departments` 
WHERE `location_id` IN(1400,1700);
	#2.查询部门中的员工姓名，要求部门号是1列表中的某一个
SELECT last_name,`department_id`
FROM `employees`
WHERE `department_id` IN (
	SELECT `department_id` 
	FROM `departments` 
	WHERE `location_id` IN(1400,1700)
	);

#题目：返回其它部门中比job_id为'IT_PROG’部门任一工资低的员工的员工号、姓名、job_id 以及salary
	#1.查询jog_id为job_id为'IT_PROG’部门中的工资
SELECT salary
FROM employees
WHERE job_id = "IT_PROG";
	#2.查询其他部门员工的工资比1最高的低的员工号、姓名、job_id 以及salary 
SELECT `employee_id`,`last_name`,`job_id`,`salary`
FROM employees
WHERE job_id <> "IT_PROG" 
AND salary < (
	SELECT MAX(salary)
	FROM employees
	WHERE job_id = "IT_PROG"
	);
	
#题目：返回其它部门中比jobid为‘T_PROG'部门所有工资都低的员工的员工号、姓名、job id以及salary
SELECT `employee_id`,`last_name`,`job_id`,`salary`
FROM employees
WHERE job_id <> "IT_PROG" 
AND salary < (
	SELECT MIN(salary)
	FROM employees
	WHERE job_id = "IT_PROG"
	);
	
	
#3.行子查询(结果集只有多列多行/一行多列)

#查询员工编号中最小的 且 工资最高的员工信息
	#1.查询最小的员工编号
SELECT MIN(`employee_id`) FROM `employees` ;
	#2.查询最高的工资
SELECT MAX(`salary`) FROM `employees`;
	#3.查询员工信息
SELECT * 
FROM `employees` 
WHERE `employee_id` = (
	SELECT MIN(`employee_id`) 
	FROM `employees` )
AND `salary` = (
	SELECT MAX(`salary`) 
	FROM `employees`);

	#利用行子查询
SELECT * 
FROM `employees` 
WHERE (`employee_id`,`salary`) = (
	SELECT MIN(`employee_id`),MAX(`salary`)
	FROM `employees`);







#二、select后面(放的子查询只能是单行单列)

#查询每个部门的员工个数
SELECT d.*,(
	SELECT COUNT(*) 
	FROM `employees` e
	WHERE e.`department_id` = d.`department_id`
	
) 个数 
FROM `departments` d;

#查询员工号=102的部门名
SELECT d.`department_name` FROM `employees` e,`departments` d WHERE e.`department_id` = d.`department_id` AND `employee_id` = 102;

#查询每个部门的平均工资,显示部门ID、部门名称和该部门的平均工资
SELECT d.`department_id`,d.`department_name`,(
	SELECT AVG(salary)
	FROM `employees` e
	WHERE d.`department_id` = e.`department_id`
) AS 部门平均工资
FROM `departments` d;

#查询每个职位的员工数量,显示职位ID和该职位的员工人数
#利用 distinct 去重
SELECT DISTINCT job_id,(
	SELECT COUNT(*) 
	FROM `employees` e2 
	WHERE e1.job_id = e2.job_id
	) AS 人数
FROM `employees` e1;

#查询每个经理管理的员工数量 显示经理ID和管理的员工人数（注意：有些员工可能没有经理）
SELECT COUNT(*),(
	SELECT `employee_id` 
	FROM `employees` e2 
	WHERE e1.`manager_id`=e2.`employee_id`
	) AS 经理id
FROM `employees` e1 
GROUP BY 经理id;

# 查询每个部门的最低工资 显示部门ID、部门名称和该部门的最低工资
SELECT `department_id`,`department_name`,(
	SELECT MIN(`salary`) 
	FROM `employees` e 
	WHERE d.`department_id` = e.`department_id`
	) AS 最低工资
FROM `departments` d ;

#查询每个部门的最高工资和最低工资的差距 显示部门ID、部门名称和工资差距
SELECT `department_id`,`department_name`,(
	SELECT MAX(`salary`) - MIN(`salary`) 
	FROM `employees` e 
	WHERE e. `department_id` = d.`department_id`
	)AS 工资差距
FROM `departments` d;


#三、from后面

/*
将子查询结果充当一张表，要求必须起别名
*/
#查询每个部门的平均工资的工资等级

#1.查询每个部门的平均工资
SELECT AVG(`salary`),`department_id` FROM `employees` GROUP BY `department_id`;
#2.连接1的结果集和job_grades表
SELECT ag_dep.*,g.grade_level
FROM (SELECT AVG(`salary`) AS ag,`department_id` FROM `employees` GROUP BY `department_id`) AS ag_dep
INNER JOIN `job_grades` g
ON ag_dep.ag BETWEEN lowest_sal AND highest_sal;



#四、exists后面(相关子查询) 是否存在

SELECT EXISTS(SELECT `employee_id` FROM `employees`); #判断子查询结果有没有值

/*
语法:
exists(完整的查询语句)
结果: 1/0
*/

#查询有员工的部门名

SELECT `department_name`
FROM `departments` d
WHERE EXISTS(
SELECT * FROM `employees` e WHERE e.`department_id` = d.`department_id`
);

#in实现
SELECT `department_name`
FROM `departments` d
WHERE d.`department_id` IN(
	SELECT `department_id`
	FROM `employees`
);

#查询没有女朋友的男神信息
USE girls;
SELECT * FROM `boys`;
SELECT * FROM beauty;

SELECT `boyName`
FROM `boys` b1
WHERE NOT EXISTS(
	SELECT * FROM `beauty` b2 WHERE b2.`boyfriend_id` = b1.`id`
	);
	
#in
SELECT bo.*
FROM boys bo
WHERE bo.id NOT IN (SELECT `boyfriend_id` FROM `beauty`);




#案例
#1查询和Z1otkey相同部门的员工姓名和工资
USE `myemployees`;
SELECT `department_id` FROM `employees`;

SELECT `employee_id`,`last_name`,`salary`
FROM `employees` e
WHERE `department_id` = (
	SELECT `department_id`
	FROM `employees`
	WHERE last_name = 'Zlotkey'
	);
	
	
	
#2.查询工资比公司平均工资高的员工的员工号，姓名和工资。
SELECT employee_id,`last_name`,`salary`
FROM `employees` e
WHERE salary > (
	SELECT AVG(salary) 
	FROM employees
	);
	
	
	
#3.查询各部门中工资比本部门平均工资高的员工的员工号，姓名和工资
	#1.求各部门的平均工资
SELECT AVG(salary) FROM employees GROUP BY `department_id`;
	#2.连接1结果集 再去进行筛选
SELECT `employee_id`,`last_name`,`salary`,`department_id`
FROM `employees` e1
WHERE salary > (
	SELECT AVG(salary)
	FROM employees e2  
	WHERE e1.`department_id` = e2.`department_id` 
	GROUP BY `department_id`
)
ORDER BY `department_id` ASC;



#4.查询姓名中包含字母u的员工在相同部门的员工的员工号和姓名

SELECT DISTINCT `department_id`
FROM `employees` 
WHERE last_name LIKE "%u%";

SELECT e1.`employee_id`,e1.`last_name` 
FROM `employees` e1
WHERE e1.`department_id` = (SELECT DISTINCT e2.`department_id`
FROM `employees` e2
WHERE e2.last_name LIKE "%u%");



#5.查询在部门的1ocationid为1700的部门工作的员工的员工号

SELECT `department_id` FROM `departments` WHERE `location_id` = 1700 ;
SELECT `employee_id` ,`last_name`
FROM `employees` e 
WHERE department_id IN (
	SELECT `department_id` 
	FROM `departments`  d
	WHERE `location_id` = 1700 AND e.`department_id` = d.`department_id`
	);

SELECT * FROM `employees`;


#6.查询管理者是King的员工姓名和工资
	#1.查询姓名为King的员工编号
SELECT `employee_id` FROM employees WHERE last_name = 'K_ing';
	#2.查询哪个员工的manager_id = 1
SELECT last_name,salary
FROM employees
WHERE manager_id IN(
	SELECT `employee_id` 
	FROM employees 
	WHERE last_name = 'K_ing'
	);



#7.查询工资最高的员工的姓名，要求first_name和last_name显示为一列，列名为姓.名
SELECT CONCAT(last_name,first_name) AS "姓.名"
FROM employees 
WHERE salary = (
	SELECT MAX(salary)
	FROM employees
	);



SELECT VERSION();


CREATE DATABASE npc_chat;

USE npc_chat;



