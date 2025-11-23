CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

-- 1. 班级表
CREATE TABLE classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_name VARCHAR(50) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 学生表
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(50) NOT NULL,
    age INT,
    gender ENUM('男', '女'),
    contact_info VARCHAR(100),
    class_id INT,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- 3. 课程表
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    credit DECIMAL(3,1) NOT NULL
);

-- 4. 选课表（学生课程关系表）
CREATE TABLE student_courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    score DECIMAL(5,2),
    selected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 插入示例数据
-- 插入班级数据
INSERT INTO classes (class_name) VALUES 
('软件1班'),
('软件2班'),
('计算机1班'),
('计算机2班');

-- 插入课程数据
INSERT INTO courses (course_id, course_name, credit) VALUES 
(1001, '数据库原理', 3.0),
(1002, '数据结构', 4.0),
(1003, '操作系统', 3.5),
(1004, '计算机网络', 3.0),
(1005, 'Java程序设计', 4.0);

-- 插入学生数据
INSERT INTO students (student_name, age, gender, contact_info, class_id) VALUES 
('张三', 20, '男', '13800138001', 1),
('李四', 21, '女', '13800138002', 1),
('王五', 19, '男', '13800138003', 2),
('赵六', 22, '女', '13800138004', 2),
('钱七', 20, '男', '13800138005', 3),
('孙八', 21, '女', '13800138006', 3),
('周九', 19, '男', '13800138007', 4),
('吴十', 22, '女', '13800138008', 4),
('郑十一', 20, '男', '13800138009', 1),
('王十二', 21, '女', '13800138010', 2);

-- 插入选课数据
INSERT INTO student_courses (student_id, course_id, score) VALUES 
(1, 1001, 85.5),
(1, 1002, 92.0),
(1, 1003, 78.5),
(2, 1001, 88.0),
(2, 1002, 76.5),
(2, 1004, 91.0),
(3, 1002, 82.0),
(3, 1003, 79.5),
(4, 1001, 95.0),
(4, 1003, 87.5),
(5, 1002, 73.0),
(5, 1004, 84.5),
(6, 1003, 89.0),
(7, 1001, 77.5),
(7, 1002, 81.0),
(8, 1003, 93.5),
(9, 1004, 86.0);



USE student_management;

1查询所有学生的姓名和所在班级名称。
SELECT student_name,`class_name`
FROM students 
INNER JOIN classes 
ON `students`.`class_id`= `classes`.`class_id`;

2查询班级名称为”软件1班”的所有学生的姓名和年龄。
SELECT student_name,`age`
FROM students 
INNER JOIN classes 
ON `students`.`class_id`= `classes`.`class_id`
WHERE `class_name` LIKE '软件1班';

3查询选修了课程ID为1002的课程的学生的姓名和所在班级名称。
SELECT `students`.`student_name`,`classes`.`class_name`
FROM `students`
JOIN `classes` ON `students`.`class_id` = `classes`.`class_id`
JOIN `student_courses` ON `student_courses`.`student_id` = `students`.`student_id`
WHERE `student_courses`.`course_id` = 1002;
		
4查询没有选修任何课程的学生的姓名和所在班级名称。
SELECT `student_name`,`class_name`
FROM `students`
JOIN `classes` ON `students`.`class_id` = `classes`.`class_id`
WHERE `students`.`student_id` NOT IN (SELECT `student_id` FROM `student_courses`);

5查询每个班级的学生数量。
SELECT COUNT(*),`classes`.`class_name`
FROM `classes` 
JOIN `students` ON `students`.`class_id` = `classes`.`class_id`
GROUP BY `classes`.`class_id`;

6查询课程ID为1003的课程的选课人数。
SELECT COUNT(*) ,`course_id` FROM `student_courses` WHERE `course_id` = 1003;

7查询学生ID为1的学生所选修的所有课程的名称。
SELECT `course_name` 
FROM `courses` 
JOIN `student_courses` ON `courses`.`course_id` = `student_courses`.`course_id` 
WHERE `student_id` = 1;

8查询学生ID为2的学生所选修的课程数量。
SELECT COUNT(*) FROM `student_courses` WHERE `student_id`=2;

9查询每个学生所选修的课程数量和总学分
SELECT COUNT(*),SUM(score) FROM `student_courses` GROUP BY `student_id`;

10查询每个学生的联系信息和所在班级名称
SELECT `student_name`,`contact_info`,`class_name` 
FROM `students` 
JOIN `classes` ON `classes`.`class_id` = `students`.`class_id`;

11查询每个班级的学生人数和平均年龄
SELECT COUNT(*),AVG(`age`) 
FROM `students` 
JOIN `classes` ON `classes`.`class_id` = `students`.`class_id`
GROUP BY `classes`.`class_id`;

12查询每门课程的选课人数和平均分数以及最高分
SELECT COUNT(*),AVG(`score`),MAX(`score`) FROM `student_courses` GROUP BY `course_id`;


