#进阶6:连接查询
/*
含义:又称为多表查询,当查询的字段来自于多个表

笛卡尔乘积现象: 表1 有m行 表2有n行 结果: m*n行

发生原因:没有有效的连接条件

如何避免:添加有效的连接条件

#分类:
	按年代分类:
		sql92标准：仅支持内连接
		sql99标准[推荐]:支持内连接,外连接(左外和右外),交叉连接
	按功能分类:
		内连接:
			等值连接
			非等值连接
			自连接
		外连接:
			左外连接
			右外连接
			全外连接
		交叉连接
*/
SELECT * FROM beauty;

SELECT * FROM boys;

SELECT NAME,boyname FROM boys,beauty WHERE beauty.`boyfriend_id` = boys.id; #笛卡尔乘积现象


#一、sql92标准
#1.等值连接
/*


1.多表等值连接的结果为多表的交集部分
2.n表连接，至少需要n-1个连接条件
3.多表的顺序没有要求
4.一般需要起别名
5.可以搭配所有查询子句


*/

#案例:查询女神名和对应的男神名

SELECT NAME,boyname 
FROM boys,beauty 
WHERE beauty.`boyfriend_id` = boys.id;

#查询员工名和对应的部门名

SELECT CONCAT(last_name,first_name) AS 姓名 ,department_name AS 部门名称
FROM employees,departments
WHERE employees.`department_id` = departments.`department_id`;

#查询工种号、员工名、工种名

#有歧义的时候可以为表起别名 起了别名查询的字段就不能使用原表名
SELECT CONCAT(last_name,first_name) AS 姓名,e.job_id 工种号,job_title 工种名
FROM employees AS e,jobs AS j
WHERE e.job_id = j.job_id;

#加筛选
#查询有奖金的员工名,部门名
SELECT last_name,department_name,`commission_pct`
FROM employees,departments
WHERE `commission_pct` IS NOT NULL AND employees.`department_id` = departments.`department_id`;

#查询城市名中第二个字符为o的部门名和城市名
SELECT * FROM departments;
SELECT * FROM `locations`;
SELECT department_name,city
FROM `departments` AS d,`locations` AS l
WHERE d.location_id = l.location_id AND l.city LIKE '_o%';

#加分组
#查询每个城市的部门个数
SELECT COUNT(*) 个数 , city 
FROM `departments` AS d,`locations` AS l
WHERE d.location_id = l.location_id
GROUP BY city;

#查询有奖金的每个部门的部门名和部门的领导编号和该部门的最低工资
SELECT `department_name`,MIN(salary),d.`manager_id`
FROM `departments` d ,`employees` e 
WHERE d.`department_id` = e.`department_id` AND e.`commission_pct` IS NOT NULL
GROUP BY `department_name`,d.`manager_id`;

#加排序
#查询每个工种的工种名和员工个数，按员工个数降序
SELECT `job_title`,COUNT(*) AS 员工个数
FROM `jobs` j ,`employees` e
WHERE j.`job_id` = e.`job_id`
GROUP BY `job_title`
ORDER BY COUNT(*) DESC;


#三表连接
#查询员工名，部门名和所在城市
SELECT last_name,department_name,city
FROM `employees` e ,`departments` d ,`locations` l
WHERE e.`department_id` = d.`department_id` 
AND d.`location_id`=l.`location_id`;


#2.非等值连接
SELECT * FROM job_grades;

CREATE TABLE job_grades
(grade_level VARCHAR(3),
 lowest_sal  INT,
 highest_sal INT);

INSERT INTO job_grades
VALUES ('A', 1000, 2999);

INSERT INTO job_grades
VALUES ('B', 3000, 5999);

INSERT INTO job_grades
VALUES('C', 6000, 9999);

INSERT INTO job_grades
VALUES('D', 10000, 14999);

INSERT INTO job_grades
VALUES('E', 15000, 24999);

INSERT INTO job_grades
VALUES('F', 25000, 40000);

#查询员工的工资和工资级别
SELECT salary,grade_level
FROM `employees` e ,job_grades j
WHERE salary BETWEEN j.lowest_sal AND j.highest_sal;


#3.自连接 自己链接自己
#查询员工名和上级的名字
SELECT e.`employee_id` AS 员工id ,e.last_name AS 员工名 ,m.manager_id AS 领导id ,m.`last_name` AS 领导名
FROM `employees` e,`employees` m
WHERE e.`manager_id` = m.`employee_id` #员工表的经理id 去找 领导表中 对应的 员工id(经理本人的员工号)





