#进阶4:一、单行函数
/*
概念:将一组逻辑语句封装在方法体中,对外暴露方法名
优点:1.隐藏了实现细节 2.提高代码的重用性
调用:select 函数名(实参列表) [from 表名];
特点: 1.叫什么(函数名)
      2.干什么(函数功能)
分类: 1.单行函数
	如 concat、length、ifnull等
      2.分组函数
	功能:做统计使用,又称为统计函数 聚合函数*/
	
#一、字符函数
#length 获取参数值的字节个数
SELECT LENGTH('john');#4
SELECT LENGTH('摇篮');#6

#concat 拼接字符
SELECT CONCAT('aa',11);
SELECT CONCAT(last_name,'_',first_name) AS 姓名 FROM employees;

#upper lower
SELECT UPPER('a');
SELECT LOWER('A');
#案例:将姓变大写 名变小写，拼接
SELECT CONCAT(UPPER(last_name),LOWER(first_name)) AS 姓名 FROM employees;

#substr substring 截取字符
SELECT SUBSTR('yyaayy',3) out_put; #索引从1开始 3-最后
SELECT SUBSTR('yyaabb',1,2) out_put; #（字符串,开始位置，截取字符长度)
#案例:姓名中首字符大写 其他字符消息 _拼接显示
SELECT CONCAT(UPPER(SUBSTR(last_name,1,1)),LOWER(SUBSTR(last_name,2)),'_',LOWER(first_name)) AS 姓名 FROM employees;

#instr 返回子串第一次出现的索引，如果找不到返回0
SELECT INSTR('杨不悔殷留下爱上了殷留下','殷留下') AS out_put;

#trim 去掉前后空格
SELECT TRIM('             张翠山       ') AS out_put;
#可以去掉前后指定字符
SELECT TRIM('a' FROM 'aaaaaaaaaaaaaaaaa张aaaaaaa翠山aaaaaaaaaaaaa') AS out_put;

#lpad 左填充指定长度的指定字符
SELECT LPAD('殷素素',10,'*') AS output;
SELECT LPAD('素殷素素',2,'*') AS output;

#rpad 右填充
SELECT RPAD('殷素素',10,'*') AS output;
SELECT RPAD('素殷素素',2,'*') AS output;

#replace 替换
SELECT REPLACE('张无忌爱上了周芷若','周芷若','赵敏') AS out_put;
SELECT REPLACE('张无忌爱上了周芷若周芷若周芷若周芷若','周芷若','赵敏') AS out_put;
SELECT REPLACE('张无忌爱上了','周芷若','赵敏') AS out_put;

#二、数学函数
#round 四舍五入
SELECT ROUND(1.65);
SELECT ROUND(1.567,2);

#ceil 向上取整
SELECT CEIL(1.52);

#floor 向下取整
SELECT FLOOR(1.02);

#truncate 截断
SELECT TRUNCATE(1.69999,1);

#mod 取模
SELECT MOD(10,3);

#三、日期函数
#now 返回当前系统日期+时间
SELECT NOW();

#curdate 返回当前系统日期，不包含时间
SELECT CURDATE();

#curtime 返回当前系统时间 不包含日期
SELECT CURTIME();

#可以获取指定的部分,年 月 日 小时 分钟 秒
SELECT YEAR(NOW());
SELECT MONTH(NOW());
SELECT MONTHNAME(NOW());
SELECT DAY(NOW());
SELECT HOUR(NOW());
SELECT MINUTE(NOW());
SELECT SECOND(NOW());

# str_to_date: 将日期格式的字符转换成指定格式的日期
SELECT STR_TO_DATE('1998-3-2','%Y-%c-%d') AS out_put;
#查询入职日期为1992-4-3的员工信息
SELECT * FROM employees WHERE hiredate = '1992-4-3';

#date_format:将日期转换成字符
SELECT DATE_FORMAT(NOW(),'%y年%m月%d日') AS out_put;
#查询有奖金的员工名和入职日期(xx月/xx日/xx年)
SELECT last_name,DATE_FORMAT(hiredate,'%m月/%d日/%y年') 入职日期 FROM employees WHERE `commission_pct` IS NOT NULL ;

#四、其他函数
SELECT VERSION();
SELECT DATABASE();
SELECT USER();

#五、流程控制函数
#if函数: 实现 if...else效果
SELECT IF(10<5,'大','小');
#查询出有没有奖金
SELECT last_name ,`commission_pct`,IF(`commission_pct` IS NULL,'没有','有') 备注 FROM employees ;

#case函数函数的使用一: switch case的效果
/*
case 要判断的字段或表达式
when 常量1 then 要显示的值1或语句1;
when 常量2 then 要显示的值1或语句2;
........
else 要显示的值n或语句n;
end
*/
#案例
/*
查询员工的工资 要求:
部门和=30  显示的工资为1.1倍
       40              1.2倍
       50              1.3倍
其他部门 显示原工资
*/
SELECT last_name ,department_id ,
CASE salary 
WHEN `department_id` = 30 THEN salary*1.1
WHEN `department_id` = 40 THEN salary*1.2
WHEN `department_id` = 50 THEN salary*1.3
ELSE salary
END AS 新工资 
FROM employees;

#case函数函数的使用二:类似 多重if
/*
case 
when 条件1 then 要显示的值1或语句1;
when 条件2 then 要显示的值2或语句2;
......
else 要显示的值n或语句n;
end
*/
#案例
/*查询员工的工资情况:
 如果工资>20000 显示A级别
 如果工资>15000 显示B级别
 如果工资>10000 显示C级别
 否则 显示D级别
*/

SELECT last_name,salary,
CASE
WHEN salary > 20000 THEN 'A'
WHEN salary > 15000 THEN 'B'
WHEN salary > 10000 THEN 'C'
ELSE 'D'
END AS 工资级别
FROM employees ORDER BY 工资级别 ASC;

#案例讲解
#1.显示系统时间（注：日期+时间）
SELECT NOW();
#2.查询员工号，姓名，工资，以及工资提高百分之20后的结果（NEWsalary）
SELECT `employee_id`,`last_name`,`salary`,`salary`*1.2 AS  "new salary" FROM employees;
#3.将员工的姓名按首字母排序，并写出姓名的长度（LENGTH）
SELECT `last_name`,LENGTH(`last_name`) AS 姓名长度 FROM employees ORDER BY `last_name` ASC;
#4.做一个查询，产生下面的结果
#<last_name> _earns <salary> monthly but wants <salary*3>
#Dream salary
#King earns 24000 monthly but wants 72000
SELECT CONCAT (last_name,' earns ',salary,'monthly but wants ', salary*3 )AS "Dream salary"FROM employees;
#5.使用CASE-WHEN，按照下面的条件：
#job   grade
#AD_PRES   A
#ST_MAN    B
#IT_PROG   c
SELECT last_name,`job_id`,
CASE
WHEN `job_id` = 'AD_PRES' THEN 'A'
WHEN `job_id` = 'ST_MAN' THEN 'B'
WHEN `job_id` = 'IT_PROG' THEN 'C'
END AS grade
FROM employees;



SELECT MD5('yy');

