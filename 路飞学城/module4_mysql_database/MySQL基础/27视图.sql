#视图
/*

含义：虚拟表,和普通表一样使用
MySQL5.1版本出现的新特性，通过表动态生成的数据


		创建语法的关键字	是否实际占用物理空间			使用
视图		create view		只保存了SQL逻辑			增删改查，一般不能增删改
表		create table		保存了数据			增删改查

*/

#案例 查询姓张的学生名和专业名

#1.直接查询
SELECT stuname,majorname
FROM stuinfo s 
INNER JOIN major m ON s.majorid=m.id
WHERE s.stuname LIKE '张%';

#2.利用视图查询
CREATE VIEW v1
AS
SELECT stuname,majorname
FROM stuinfo s 
INNER JOIN major m ON s.majorid=m.id;

SELECT * FROM v1 WHERE stuname LIKE '张%';


#一、创建视图

USE myemployees;
/*
语法：
	create view 视图名
	as
	查询语句;
*/

#1.查询姓名中包含a字符的员工名、部门名和工种信息
#①创建视图
CREATE VIEW myv1
AS 
SELECT DISTINCT `last_name`,`department_name`,`job_title` 
FROM `departments` d,`employees` e,`jobs` j
WHERE d.`department_id` = e.`department_id` AND e.`job_id` = j.`job_id` ;

#②使用视图
SELECT * FROM myv1 WHERE last_name LIKE'%a%';


#2.查询各部门的平均工资级别
#①创建视图 查询各部门的平均工资
CREATE VIEW myv2
AS 
SELECT `department_name`,AVG(salary) AS a_vg
FROM `employees` e
JOIN `departments` d ON e.`department_id` = d.`department_id`
GROUP BY `department_name`;

#②使用视图查询平均工资的级别
SELECT `department_name` ,`grade_level`
FROM myv2,`job_grades` 
WHERE myv2.a_vg BETWEEN `lowest_sal` AND `highest_sal`;


#3.查询平均工资最低的部门信息
CREATE VIEW myv3
AS 
SELECT d.`department_id`,`department_name`,d.`manager_id`,`location_id`,AVG(salary) AS a_vg
FROM `employees` e
JOIN `departments` d ON e.`department_id` = d.`department_id`
GROUP BY d.`department_id`,`department_name`,d.`manager_id`,`location_id`;

SELECT * 
FROM myv3 
ORDER BY a_vg ASC 
LIMIT 1;

#4.查询平均工资最低的部门名和工资
CREATE VIEW myv4
AS 
SELECT `department_name`,AVG(salary) AS a_vg
FROM `employees` e
JOIN `departments` d ON e.`department_id` = d.`department_id`
GROUP BY `department_name`;

SELECT * FROM myv4 ORDER BY a_vg ASC LIMIT 1;


#二、视图的修改

/*
语法：
	方式一：
	create or replace view 视图名
	as 
	查询语句;
	方式二：
	alter view 视图名
	as
	查询语句;
*/

#修改myv3
#方式一：
SELECT * FROM myv3;
CREATE OR REPLACE VIEW myv3
AS SELECT AVG(salary),job_id
FROM employees
GROUP BY job_id;
#方式二：
ALTER VIEW myv3
AS SELECT * FROM employees;


#三、删除视图

/*
语法：
	drop view 视图名，视图名,....;

*/

DROP VIEW myv3;

#四、查看视图结构

DESC myv4;
SHOW CREATE VIEW myv4;


#案例讲解
#一、创建视图emp_1，要求查询电话号码以011开头的员工姓名和工资、邮箱
CREATE VIEW emp_1
AS 
SELECT `last_name`,`salary`,`email`,`phone_number`
FROM employees;

SELECT `last_name`,`email`,`salary` FROM emp_1 WHERE `phone_number` LIKE '011%';
#二、创建视图emp_v2，要求查询部门的最高工资高于12000的部门信息

CREATE VIEW emp_v2 
AS 
SELECT MAX(salary) AS m_ax,d.`department_id`,`department_name`
FROM `employees` e
JOIN `departments` d ON e.`department_id` = d.`department_id`
GROUP BY d.`department_id`,`department_name`
HAVING m_ax > 12000;

SELECT * FROM emp_v2;


#五、视图的更新
CREATE OR REPLACE VIEW myv1
AS 
SELECT last_name,email
FROM employees;

SELECT * FROM myv1;

#1.插入
INSERT INTO myv1 VALUES('张飞','zf@qq.com',1000000000);#'annual salary'列不可更新

INSERT INTO myv1 VALUES('张飞','zf@qq.com');

#修改
UPDATE myv1 SET last_name = '飞飞公主' WHERE last_name = '张飞';

#删除
DELETE FROM myv1 WHERE last_name = '飞飞公主';

/*
具备一下特点的视图不允许更新

包含以下关键字的SQL语句：
分组函数、DISTINCT、GROUP BY、HAVING、UNION或者UNION ALL`chat_history`
常量视图
SELECT中包含子查询
JOIN
FROM一个不能更新的视图
WHERE子句的子查询引用了FROM子句中的表

*/








