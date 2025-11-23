#存储过程和函数
/*
存储过程和函数:类似方法
优点:
	1.提高代码的重用性
	2.简化操作
*/

#一、存储过程:一组预先编译好的SQL语句的集合，理解成批处理语句
/*
1.提高代码的重用性
2.简化操作
3.减少了编译次数以及和数据库服务的连接次数，提高了效率
*/

#1、创建语法
CREATE PROCEDURE 存储过程名(参数列表)
BEGIN
	存储过程体(一组SQL语句)
END;

注意:
	1.参数列表：参数模式 参数名 参数类型
	    举例：     IN   stuname VARCHAR(20);
	    参数模式:
		IN :该参数可以作为输入，也就是该参数需要调用方传入值
		OUT :该参数可以作为输出，也就是该参数可以作为返回值
		INOUT:该参数可以作为输入输出，也就是即需要传入值，也可以返回值
	2.如果存储过程体只有一句话 BEGIN END 可以省略
	  存储过程体的每条SQL语句的结尾要求必须加;
	  存储过程的结尾可以使用 DELIMITER 重新设置
	  语法： DELIMITER 结束标记
	  案例: DELIMITER $
	  
#2、使用语法
CALL 存储过程名(实参列表);


#3、案例
#①空参列表
#插入到admin表中五条记录


DELIMITER $
CREATE PROCEDURE myp1()
BEGIN
	INSERT INTO ADMIN(username,`password`)
	VALUES('john1','00000'),
	('lili','00000'),
	('mike','00000'),
	('rose','00000'),
	('tom','00000');
END $

CALL myp1()$  #调用

#②创建带in模型参数的存储过程
#根据女神名，查询对应的男神信息
CREATE PROCEDURE myp2(IN beautyName VARCHAR(20))
BEGIN
	SELECT bo.*
	FROM boys bo
	RIGHT JOIN beauty b ON bo.id = b.`boyfriend_id`
	WHERE b.name = beautyName;
END $

CALL myp2('常量值')$  #调用


#实现用户是否登陆成功
SELECT * FROM ADMIN;
INSERT INTO ADMIN(`username`,`password`)VALUES('john','8888'),('john','8888'),('john','8888'),('john','8888');
DELIMITER $
CREATE PROCEDURE myp4(IN input_username VARCHAR(20),input_password VARCHAR(20))
BEGIN
	DECLARE result INT DEFAULT 0;#声明并初始化

	SELECT COUNT(*) INTO result #赋值
	FROM ADMIN
	WHERE admin.`username` = input_username AND admin.`password` = input_password;
	
	SELECT IF (result > 0 ,'yes','no');#使用
END $

CALL myp4('john','8888')$


#③创建带out模型参数的存储过程
CREATE PROCEDURE myp5(IN beautyName VARCHAR(20),OUT boyName VARCHAR(20))
BEGIN

	SELECT `boys`.`boyName` INTO boyName
	FROM `boys` 
	RIGHT JOIN`beauty` ON `beauty`.`boyfriend_id` = `boys`.`id` 
	WHERE `beauty`.`name` = beautyName;
	
	
END $

SET @bname$ #定义一个变量用来接收boyName的返回值 只有用set定义用户变量 才能在外部定义
CALL myp5('王语嫣',@bname)$#调用

SELECT @bname$


#根据女神名返回男神名以及魅力值
CREATE PROCEDURE myp6(IN beautyName VARCHAR(20),OUT boyName VARCHAR(20),OUT usercp INT)
BEGIN
	SELECT `boys`.`boyName` ,`boys`.`userCP` INTO boyName,usercp
	FROM boys
	RIGHT JOIN beauty ON `beauty`.`boyfriend_id` = `boys`.`id` 
	WHERE `beauty`.`name` = beautyName;
END$
CALL myp6('王语嫣',@bname,@usercp)$#调用
SELECT @bname,@usercp$

#④创建带inout模式参数的存储过程
#传入a,b 要求a,b翻倍并返回

CREATE PROCEDURE myp7(INOUT a INT,INOUT b INT)
BEGIN
	#select  a*2 , b*2 into a,b;#错误 into子句只能将查询结果赋值给变量或用户变量，不许给存储过程参数
	SET a = a*2;
	SET b = b*2;
END$
SET @a = 3;
SET @b = 4;
#call myp7(3,4)$#不能直接传入常量 因为INOUT 参数需要既能传入值又能传出值
CALL myp7(@a,@b)$




#案例讲解
#1.创建存储过程或函数实现传入用户名和密码，插入到admin表中
CREATE PROCEDURE myp8(IN uname VARCHAR(20),IN pwd VARCHAR(20))
BEGIN
	INSERT INTO ADMIN(`username`,`password`)VALUES(uname,pwd);
END$
CALL myp8()$
#2.创建存储过程或函数实现传入女神编号，返回女神名称和女神电话
CREATE PROCEDURE myp9(IN beautyId INT, OUT beautyName VARCHAR(20),OUT bnum VARCHAR(20) )
BEGIN
	SELECT `name`,`phone` INTO beautyName,bnum FROM `beauty` WHERE`id` = beautyId  ;
	
END$
CALL myp9(2,@bname,@bnum)$
SELECT @bname,@bnum$

#3.创建存储存储过程或函数实现传入两个女神生日，返回大小
CREATE PROCEDURE myp10(IN a DATE,IN b DATE)
BEGIN

	SELECT a,IF (a > b ,'>',IF(a < b ,'<','=')) ,b;
END$

CALL myp10('1999-8-1','1998-8-1')$
 
#老师的方法
CREATE PROCEDURE myp11(IN birth1 DATETIME,IN birth2 DATETIME,OUT result INT)
BEGIN
	SELECT DATEDIFF(birth1,birth2) INTO result;
END$

CALL myp11('1998-7-7',NOW(),@result)$

DELIMITER ;


#4、存储过程的删除
#语法：drop procedure 存储过程名 (一次只能删除一个)

DROP PROCEDURE myp1;


#5、查看存储过程的信息结构
SHOW CREATE PROCEDURE myp10;


#案例讲解
DELIMITER $
#4.创建存储过程或函数实现传入一个日期，格式化成xx年xx月xx日并返回
CREATE PROCEDURE myp12(INOUT adate VARCHAR(20))
BEGIN

	SET adate =  DATE_FORMAT(adate,'%y年/%m月/%d日') 
	
END $
SET @adate = '1998-8-1'$
CALL myp12(@adate)$


#5.创建存储过程或函数实现传入女神名称，返回：女神AND男神格式的字符串
如传入：小昭
返回：小昭AND张无忌
CREATE PROCEDURE myp13(IN beautyName VARCHAR(20),OUT bbname VARCHAR(20))
BEGIN
	#select concat(b1.name,'and',b2.boyName) into bbname #若boyName是null 则整体都是null
	SELECT CONCAT(b1.name,'and',IFNULL (b2.boyName , 'null')) INTO bbname #拼接字符串null可以避免这种情况

	FROM `beauty` b1 
	JOIN `boys` b2 ON b1.`boyfriend_id` = b2.id
	WHERE beautyName = b1.name;
END$

CALL myp13('周冬雨',@bbname)$



#6.创建存储过程或函数，根据传入的条目数和起始索引，查询beauty表的记录
CREATE PROCEDURE myp14(IN n INT, IN st_index INT)
BEGIN
	SELECT * FROM beauty LIMIT st_index,n;
END$

CALL myp14(3,2)$




#二、函数
/*
一组预先编译好的SQL语句的集合，理解成批处理语句

1.提高代码的重用性
2.简化操作
3.减少了编译次数以及和数据库服务的连接次数，提高了效率

区别：
	存储过程：可以有0个返回，也可以有多个返回，适合做批量插入、更新
	函数：有且仅有1个返回，适合做处理数据后返回一个结果
*/

#1.创建语法
CREATE FUNCTION 函数名(参数列表) RETURNS 返回类型
BEGIN
	函数体
END
/*
注意:1.参数列表： 参数名 参数类型
     2.函数体：肯定会有return语句，如果没有会报错
		如果return语句没有放在函数体的最后也不会报错，但不建议
		return 值;
     3.函数体只有一句话，可以省略begin end
     4.使用delimiter语句设置结束标记

*/

#2.调用语法
SELECT 函数名(参数列表);


#3.案例
#无参有返回
#返回公司的员工个数
CREATE FUNCTION myf1() RETURNS INT
BEGIN
	DECLARE c INT DEFAULT 0;#定义一个变量
	SELECT COUNT(*) INTO c #赋值
	FROM employees;
	RETURN c;
END $

SELECT myf1()$

#有参有返回
#根据员工名返回他的工资
CREATE FUNCTION myf2( ename VARCHAR(20)) RETURNS FLOAT
BEGIN
	DECLARE s FLOAT DEFAULT 0;#定义局部变量
	SELECT salary INTO s
	FROM employees
	WHERE last_name = ename;
	RETURN s;
END$

SELECT myf2('K_ing')$

#根据部门名，返回该部门的平均工资
CREATE FUNCTION myf3(deptName VARCHAR(20)) RETURNS FLOAT
BEGIN
	SET @sal = 0;#定义用户变量
	SELECT AVG(salary) INTO @sal  FROM `departments` d JOIN `employees` e ON d.`department_id` = e.`department_id`
	WHERE deptName = `department_name`;
	RETURN @sal;
END$

SELECT myf3('Adm')$

#3.查看函数
DELIMITER ;
SHOW CREATE FUNCTION myf3;

#4.删除函数
DROP FUNCTION myf3;


#案例
#1.创建函数，实现传入两个float,返回和
DELIMITER $
CREATE FUNCTION myf4(a FLOAT ,b FLOAT) RETURNS DOUBLE
BEGIN
	DECLARE s DOUBLE DEFAULT 0;
	SET s = a +b;
	RETURN s;
END$

SELECT myf4(1.2,2.2)$



