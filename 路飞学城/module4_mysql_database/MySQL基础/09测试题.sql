#一、显示员工表的最大工资，工资平均值
SELECT MAX(salary),AVG(salary) FROM employees;

#二、查询员工表的employee_id,job_id,last_name，按department_id降序，salary升序
SELECT `employee_id`,`job_id`,`last_name`
FROM `employees`
ORDER BY `department_id` DESC,`salary` ASC;

#三、查询员工表的job_id中包含a和e的，并且a在e的前面
SELECT `job_id` FROM employees WHERE job_id LIKE '%a%e%';

#四、已知表student，里面有id(学号)，name，gradeId、（年级编号）
#已知表grade,里面看id(年级编号)’,name(年级名)
#已知表result，重面有id,score,studentNo(学号）
#查询姓名、年纪名、成绩
SELECT r.name,g.name,score
FROM grade g ,result r ,student s 
WHERE s.gradeId = g.id AND s.id = r.studentNo;

#五、显示当前日期，以及去前后空格，截取子字符串的函数
SELECT NOW();
SELECT TRIM("")
SELECT SUBSTR(str,startindex)
SELECT SUBSTR(str,startindex,LENGTH)









#作业
#1显示所有员工的姓名，部门号和部门名称。

SELECT last_name,e.`department_id`,d.`department_name`
FROM `employees` e ,`departments` d 
WHERE e.`department_id` = d.`department_id`;



#2查询90号部门员工的job_id和90号部门的1ocation_id

SELECT e.job_id,d.location_id
FROM `employees` e,`departments` d
WHERE e.`department_id` = d.`department_id` AND e.`department_id`=90
GROUP BY `job_id`,`location_id`



#3.选择所有有奖金的员工的
#last_name,department_name.location_id， city

SELECT e.last_name AS 员工名 ,d.department_name AS 部门名称 ,l.location_id AS 地址id,l.city AS 城市
FROM `employees` e ,`departments` d ,`locations` l
WHERE e.`department_id` = d.`department_id` 
AND d.`location_id` = l.`location_id` 
AND `commission_pct` IS NOT NULL;



#4.选择city在Toronto工作的员工的
#last_name , job_id， department_id， department_name

SELECT e.last_name,e.job_id,d.department_id,d.department_name,city
FROM employees e,departments d,locations l
WHERE e.department_id = d.department_id AND d.location_id = l.location_id AND l.city IN ("Toronto");



#5.查询每个工种、每个部门的部门名、工种名和最低工资

SELECT job_title 工种名,department_name 部门名,MIN(salary) 最低工资
FROM employees e ,departments d ,jobs j 
WHERE e.department_id = d.department_id AND e.job_id = j.job_id
GROUP BY `job_title`,`department_name`;



#6.查询每个国家下的部门个数大于2的国家编号

SELECT `country_id`,COUNT(*) AS 个数
FROM locations l,departments d
WHERE d.location_id = l.location_id
GROUP BY `country_id` #group by后面不能放聚合函数 个数>2并不是分组依据而是分组后的筛选条件 应该放在having 后面
HAVING 个数 > 2;



#7、选择指定员工的姓名，员工号，以及他的管理者的姓名和员工号，结果类似于下面的格式
#employees        Emp#          manager             Mgr#
#kochhar           101          king                100

SELECT e.last_name AS employees ,e.`employee_id` AS "Emp#" ,m.`last_name` AS manager,m.`manager_id` AS "Mgr#"
FROM  employees e,employees m
WHERE e.`manager_id` = m.employee_id;




















