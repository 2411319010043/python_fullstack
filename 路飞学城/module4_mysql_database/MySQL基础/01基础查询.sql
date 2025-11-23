#进阶1:基础查询
/*
语法:
SELECT 查询列表 FROM 表名;
特点：
1、查询列表可以是:表中的字段、常量值、表达式、函数
2、查询到结果是一个虚拟的表格
*/
USE myemployees;

#1.查询表中的单个字段
SELECT last_name FROM employees;

#2.查询表中的多个字段
SELECT last_name,salary,email FROM employees;

#3.查询表中的所有字段
SELECT * FROM employees;

#4.查询常量值
SELECT 100;
SELECT 'john';

#5.查询表达式
SELECT 100*98;
SELECT 100%98;

#6.查询函数
SELECT VERSION();

#7.起别名
/*
1.便于理解
2.如果要查询的字段有重名的情况，使用别名可以区分
*/
#方式一：
SELECT 100%98 AS 结果;
SELECT last_name AS 姓,first_name AS 名 FROM employees;
#方式二：
SELECT last_name 姓,first_name 名,phone_number 电话 FROM employees;
#案例: 查询salary，显示结果为: out put
SELECT salary "out put" FROM employees;

#8.去重
#案例:查询员工表中涉及到的所有的部门编号
SELECT DISTINCT department_id FROM employees;

#9.+号的作用
/*
运算符

select 100+90; 两个操作数都为数值型,做加法运算
select '123'+90; 其中一方为字符型，试图将字符型数值转为数值型
			若转换成功，则继续做加法运算
select 'john'+90;	若转换失败，则将字符型数值转为0
select 'john'+null; 只要一方为null，结果肯定为null
*/

#案例：

#查询员工的名和姓连接成一个字段，并显示为 姓名
SELECT CONCAT('a','b','c') AS 结果;
SELECT CONCAT(last_name,first_name) AS 姓名 FROM employees;

#显示departments表结构，并查询全部数据
DESC departments;
SELECT * FROM departments;

#显示出表employees中的全部job_id(不能重复)
SELECT DISTINCT job_id FROM employees;

#显示出表employees的全部列，各个列之间用逗号连接，列头显示成OUT_PUT
SELECT 
	CONCAT(`first_name`,',',`last_name`,',',IFNULL(`commission_pct`,0)) AS OUT_PUT 
FROM employees;

#补充 ifnull 如果值为null 则显示....
SELECT IFNULL(`commission_pct`,0) AS 奖金率 ,`commission_pct` 
FROM employees;