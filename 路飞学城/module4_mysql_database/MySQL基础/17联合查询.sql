#进阶9:联合查询
/*
union 联合 合并:将多条查询语句的结果合并成一个结果

语法:
	查询语句1
	union
	查询语句2
	union
	....
	
应用场景:
	要查询的结果来自于多个表，且多个表没有直接的连接关系，但查询的信息一致时
	
特点:
	1.要求多条语句的查询列数一致
	2.要求多条查询语句的查询的每一列的类型和顺序最好一致
	3.单独使用union语句时若多表中有重复的数据会自动去重，若不想去重 可用union all
*/

USE myemployees;

#引入的案例；查询部门编号>90,或邮箱中包含a的员工信息
SELECT * FROM `employees` WHERE `department_id` >90 OR `email` LIKE"%a%";

SELECT * FROM `employees` WHERE `email` LIKE"%a%"
UNION
SELECT * FROM `employees` WHERE `department_id` >90;








