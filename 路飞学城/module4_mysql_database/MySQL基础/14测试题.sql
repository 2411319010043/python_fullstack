已知表 stuinfo
id学号
NAME 姓名
email 邮箱, john@126.com 
gradeId 年级编号
sex 性别 男 女
age 华龄

己知表 grade
id 年级编号
gradeName 年级名称

一、查询所有学员的邮箱的用户名（注：邮箱中@前面的字符）
instr返回@的位置 包含了字符@ 应该-1 只取用户名
SUBSTR(email,1,INSTR(email,'@')-1) FROM stuinfo;

二、查询男生和女生的个数

SELECT sex AS 性别,COUNT(*) AS 人数 FROM stuinfo GROUP BY sex ;

三、查询年龄>18岁的所有学生的姓名和年级名称

SELECT NAME,gradeName FROM stuinfo s ,grade  g WHERE s.gradeId = g.id AND age>18;

四、查询哪个年级的学生最小年龄>20岁

SELECT gradeName FROM stuinfo s ,grade g WHERE s.gradeId = g.id GROUP BY g.id HAVING MIN(age)>20;

五、试说出查询语句中涉及到的所有的关键字，以及执行先后顺序
SELECT 查询列表  7
FROM 表1  1
JOIN 表2  2
ON 连接条件  3
WHERE 筛选条件  4
GROUP BY 分组   5
HAVING 分组后筛选条件   6
ORDER BY 排序  8
LIMIT 分页  9





