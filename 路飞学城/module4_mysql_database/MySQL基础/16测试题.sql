#作业
USE `myemployees`;



#1.查询工资最低的员工信息：last_name，salary

	#1.先找出最低的工资
SELECT MIN(salary) FROM employees;
	#2.查询last_name，salary 要求salary = ①
SELECT last_name,salary 
FROM employees 
WHERE salary = (SELECT MIN(salary) FROM employees);



#2.♥♥♥查询平均工资最低的部门信息。 利用内连接
	#1.查询各部门平均工资
SELECT AVG(salary) ,`department_id`FROM `employees` GROUP BY `department_id`;
	#2.查询①结果的最低平均工资
SELECT MIN(ag)
FROM (
	SELECT AVG(salary)  AS ag ,`department_id`
	FROM `employees` 
	GROUP BY `department_id`
)AS ag_dep;
	#3.查询哪个部门的平均工资=②
SELECT AVG(salary),`department_id`
FROM `employees`
GROUP BY `department_id`
HAVING AVG(salary) = (SELECT MIN(ag)
FROM (
	SELECT AVG(salary)  AS ag ,`department_id`
	FROM `employees` 
	GROUP BY `department_id`
)AS ag_dep);
	#4.查询这个部门的部门信息
SELECT d.*
FROM `departments` d 
WHERE d.`department_id` = (
	SELECT `department_id`
	FROM `employees`
	GROUP BY `department_id`
	HAVING AVG(salary) = (
		SELECT MIN(ag)
		FROM (
			SELECT AVG(salary)  AS ag ,`department_id`
			FROM `employees` 
			GROUP BY `department_id`
		)AS ag_dep
	)
);


#自己写的
SELECT * 
FROM departments d
WHERE d.department_id = (
    SELECT department_id 
    FROM employees 
    GROUP BY department_id 
    ORDER BY AVG(salary) ASC 
    LIMIT 1
);
		     



#3.查询平均工资最低的部门信息和该部门的平均工资。

	#1.计算每个部门的平均工资
SELECT AVG(salary) AS avg_salary ,department_id FROM employees GROUP BY `department_id`;
	#2.从所有部门的平均工资中，找出最小值  (1) 按照工资排序 
SELECT AVG(salary) AS avg_salary ,department_id FROM employees GROUP BY `department_id` ORDER BY avg_salary ASC LIMIT 0,1;
	#3.定位到这个最低平均工资对应的部门
SELECT department_id FROM employees WHERE department_id = 
	#4.获取该部门的详细信息
SELECT d.department_id, d.department_name, d.manager_id, d.location_id,dept_avg.avg_salary
FROM (
	SELECT AVG(salary) AS avg_salary ,department_id 
	FROM employees GROUP BY `department_id` 
	ORDER BY avg_salary ASC 
	LIMIT 0,1
	) AS dept_avg
INNER JOIN departments d
ON d.`department_id` = dept_avg.`department_id`;


SELECT * 
FROM `departments` d,(
	SELECT AVG(salary) AS avg_salary ,department_id 
	FROM employees GROUP BY `department_id` 
	ORDER BY avg_salary ASC 
	LIMIT 0,1
	) AS dept_avg
WHERE d.`department_id` = dept_avg.`department_id`;



#4.查询平均工资最高的job(工种) 信息。
SELECT * FROM jobs;
	#1.先查询每个工种的平均工资
SELECT AVG(salary),job_id FROM employees GROUP BY job_id;
	#2.#2.从所有部门的平均工资中，找出最高  (1) 按照工资排序 
SELECT AVG(salary) AS avg_salary ,job_id FROM employees GROUP BY job_id ORDER BY avg_salary DESC;
	#3.定位到这个最低平均工资对应的部门
SELECT AVG(salary) AS avg_salary ,job_id FROM employees GROUP BY job_id ORDER BY avg_salary DESC LIMIT 1;
	#4.
SELECT j.`job_id`,`job_title`,`min_salary`,`max_salary` FROM (SELECT AVG(salary) AS avg_salary ,job_id FROM employees GROUP BY job_id ORDER BY avg_salary DESC LIMIT 1)
 AS e INNER JOIN jobs j ON e.job_id  = j.job_id ;
 
 
#5.查询平均工资高于公司平均工资的部门有哪些？

SELECT department_id, AVG(salary) AS 部门平均工资
FROM employees 
GROUP BY department_id
HAVING AVG(salary) > (SELECT AVG(salary) FROM employees);

#6.查询出公司中所有manager的详细信息.

#自连接
#自连接
#查询员工名和上级的名字 姓名中包含字符k的
#SELECT e.`last_name`,m.`last_name`
#FROM `employees` e
#JOIN `employees` m ON e.`manager_id` = m.`employee_id`
#WHERE e.last_name LIKE '%k%';

SELECT DISTINCT `manager_id` FROM `employees`;

SELECT DISTINCT m.`last_name`,m.`first_name`,m.`email`,m.`phone_number`
FROM employees e
JOIN employees m ON e.manager_id = m.`employee_id`;




#7.各个部门中最高工资中最低的那个部门的最低工资是多少
	#1.先找出各个部门中最高工资的排序
SELECT MAX(salary) AS 最高工资,`department_id` 
FROM `employees` 
GROUP BY `department_id` 
ORDER BY 最高工资 ASC LIMIT 1;



#8.查询平均工资最高的部门的manager的详细信息：lastname，department id，email salaryw
#	1.查询各个部门的平均工资
SELECT `department_id` 
FROM `employees` 
GROUP BY `department_id` 
ORDER BY AVG(salary) DESC LIMIT 1;

#	2.显示部门的manager的id
SELECT manager_id FROM `departments` d ,(SELECT `department_id` 
FROM `employees` 
GROUP BY `department_id` 
ORDER BY AVG(salary) DESC LIMIT 1) AS  a WHERE d.`department_id` = a.`department_id`;
# 找出employees表中manager_id 对应的员工id
SELECT `last_name`,`department_id`,`email`,`salary` FROM `employees` e ,(SELECT manager_id FROM `departments` d ,(SELECT `department_id` 
FROM `employees` 
GROUP BY `department_id` 
ORDER BY AVG(salary) DESC LIMIT 1) AS  a WHERE d.`department_id` = a.`department_id`) AS b WHERE e.`employee_id` = b.`manager_id`;

#以下是student表的作业 先创建student表

CREATE DATABASE IF NOT EXISTS student;
USE student;


-- 专业表
CREATE TABLE major (
    majorid INT PRIMARY KEY,      -- 专业ID
    majorname VARCHAR(50) NOT NULL -- 专业名称
);

INSERT INTO major (majorid, majorname) VALUES
(1, '计算机科学'),
(2, '物理学'),
(3, '文学'),
(4, '空灵艺术'); -- 这个专业没有学生，用于第10题

-- 学生表
CREATE TABLE student (
    studentid INT PRIMARY KEY,    -- 学生ID
    sname VARCHAR(50) NOT NULL,   -- 学生姓名
    sex CHAR(1),                  -- 性别
    borndate DATE,                -- 生日
    phone VARCHAR(20),            -- 电话
    email VARCHAR(100),           -- 邮箱 (用于第8题)
    majorid INT,                  -- 专业ID (外键)
    userpwd VARCHAR(50)           -- 密码 (用于第7题)
);

INSERT INTO student (studentid, sname, sex, borndate, phone, email, majorid, userpwd) VALUES
(1, '张三丰', '男', '1987-05-01', '13800138001', 'zhangsanfeng@email.com', 1, 'abc123'),
(2, '张翠山', '男', '1989-08-15', '13800138002', 'cuishan@email.com', 1, 'abc123'),
(3, '张无忌', '男', '1990-12-25', '13800138003', 'wuji.zhang@email.com', 2, 'abc123'),
(4, '李秋水', '女', '1988-03-10', '13800138004', 'liqiushui@email.org', 2, 'abc123'),
(5, '周芷若', '女', '1989-11-05', '13800138005', 'zhirozhou@email.net', 3, 'abc123'),
(6, '宋远桥', '男', '1987-01-20', '13800138006', 'songyq@email.com', 3, 'abc123'),
(7, '杨不悔', '女', '1991-07-30', NULL, NULL, NULL, 'abc123'); -- 这个学生没有专业和成绩，用于第11题

-- 课程表
CREATE TABLE course (
    courseid INT PRIMARY KEY,     -- 课程ID
    coursename VARCHAR(50) NOT NULL -- 课程名称
);

INSERT INTO course (courseid, coursename) VALUES
(1, '高等数学'),
(2, '大学英语'),
(3, '程序设计');

-- 成绩表
CREATE TABLE score (
    scoreid INT PRIMARY KEY,      -- 成绩ID
    studentid INT NOT NULL,       -- 学生ID (外键)
    courseid INT NOT NULL,        -- 课程ID (外键)
    score INT                     -- 分数
);

INSERT INTO score (scoreid, studentid, courseid, score) VALUES
(1, 1, 1, 85),
(2, 1, 2, 78),
(3, 1, 3, 92),
(4, 2, 1, 58),  -- 张翠山有不及格的成绩
(5, 2, 2, 72),
(6, 2, 3, 65),
(7, 3, 1, 90),
(8, 3, 2, 88),
(9, 3, 3, 95),
(10, 4, 1, 62),
(11, 4, 2, 70),
(12, 4, 3, 68),
(13, 5, 1, 95),
(14, 5, 2, 92),
(15, 5, 3, 98),
(16, 6, 1, 55), -- 宋远桥有不及格的成绩
(17, 6, 2, 60),
(18, 6, 3, 59);
-- 注意：学生 '杨不悔' (studentid=7) 没有任何成绩记录






#下面是练习题

一、查询每个专业的学生人数

SELECT COUNT(*) ,`majorname` 
FROM `student` s ,`major` m 
WHERE m.`majorid` = s.`majorid` 
GROUP BY s.`majorid`;

二、查询参加考试的学生中，每个学生的平均分、最高分

#1.先查出谁参加考试了
SELECT DISTINCT `sname` FROM `student` s1 , `score` s2 WHERE s1.`studentid` = s2.`studentid`; 

#2.查出学生的平均分、最高分
SELECT AVG(score) ,MAX(score) FROM `score` GROUP BY `studentid`;

#3.将1 2 连接
SELECT AVG(score) ,MAX(score) ,sname 
FROM `score` s1, student s2 
WHERE s1.`studentid` = s2.`studentid` 
GROUP BY s1.`studentid`;

三、查询姓张的每个学生的最低分大于60的学号、姓名

SELECT s1.`studentid`,`sname` 
FROM `score` s1,`student` s2 
WHERE s2.`studentid` = s1.`studentid` AND `sname` LIKE "张%" 
GROUP BY s1.studentid 
HAVING MIN(score) > 60;


四、查询每个专业生日在”1988-1-1”后的学生姓名、专业名称


SELECT s.sname,m.`majorname`,`borndate`
FROM `student` s ,`major` m 
WHERE m.`majorid` = s.`majorid` AND `borndate` > "1988-1-1";


五、查询每个专业的男生人数和女生人数分别是多少
	#1.自己写的0人的专业不会被查询出来

SELECT m.`majorname`,SUM(CASE WHEN s.sex = '男' THEN 1 ELSE 0 END ) AS male,SUM(CASE WHEN s.sex = '女' THEN 1 ELSE 0 END ) AS female
FROM student s ,`major` m WHERE m.`majorid` = s.`majorid` GROUP BY m.`majorid`,`majorname`;

	#2.利用左连接 让左边的major当主表 保留所有的专业

SELECT m.`majorname`，
	SUM(CASE WHEN s.sex = '男' THEN 1 ELSE 0 END) AS female,
	SUM(CASE WHEN s.sex = '女' THEN 1 ELSE 0 END) AS male
FROM `major` m 
LEFT JOIN `student` s ON m.`majorid` = s.`majorid` 
GROUP BY m.`majorid`,m.`majorname`;


六、查询专业和张翠山一样的学生的最低分

SELECT COUNT(*) FROM `major` m ,`student` s WHERE s.`majorid` = m.`majorid` AND`majorname` = "计算机科学" GROUP BY m.`majorid`;
#1.先查出张翠山的专业
SELECT m.`majorid` FROM `major` m INNER JOIN `student` s WHERE s.`majorid` = m.`majorid` AND sname = "张翠山";
#2.查出和张翠山一样专业的学生
SELECT MIN(score)
FROM `score` s2
INNER JOIN `student` s3 
WHERE s2.`studentid` = s3.`studentid` AND s3.`majorid` = (
	SELECT m.`majorid` 
	FROM `major` m 
	INNER JOIN `student` s 
	WHERE s.`majorid` = m.`majorid` AND sname = "张翠山"
	);

七、查询大于60分的学生的姓名，密码、专业名

#1.查出大于60分的学生的姓名和密码
SELECT DISTINCT `sname`,`userpwd`,`majorname`  
FROM `student` s1,`major` m,`score` s2
WHERE s1.`majorid` = m.`majorid` AND s1.`studentid` =s2.`studentid` AND `score` > 60;

八、按邮箱位数分组，查询每组的学生个数

SELECT COUNT(*) AS 学生个数 ,LENGTH(email) 邮箱位数 FROM `student` GROUP BY LENGTH(email) ;



九、查询学生名、专业名、分数
SELECT  sname,majorname,score FROM `student` s1,`major` m,`score` s2 WHERE s1.`studentid` = s2.`studentid` AND s1.`majorid` = m.`majorid`;

十、查询哪个专业没有学生，分别用左连接和右连接实现

#1.左连接
SELECT `majorname` 
FROM major m 
LEFT JOIN `student` s ON m.`majorid` = s.`majorid` 
WHERE s.majorid IS NULL;
#2.右连接
SELECT majorname 
FROM student s 
RIGHT JOIN major m ON m.majorid = s.majorid 
WHERE s.majorid IS NULL;

十一、查询没有成绩的学生人数 隐形或者内连接都不行 因为只找出交集 而我们要做的事以学生表为主表 
SELECT COUNT(*) 
FROM `student` s1 
LEFT JOIN`score` s2 ON s1.`studentid` = s2.`studentid` 
WHERE s2.`score` IS NULL;


























