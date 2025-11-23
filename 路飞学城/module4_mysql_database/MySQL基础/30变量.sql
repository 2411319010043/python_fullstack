#变量
/*
分类：1.系统变量：
	          全局变量
	          会话变量
      2.自定义变量:
		  用户变量
		  局部变量
*/

#一、系统变量

/*变量由系统提供，不是用户定义，属于服务器层面

作用域：
	服务器每次启动将为所有的全局变量,针对于所有的会话(连接)有效,但是不能跨重启

语法：
	1.查看所有的系统变量
	show global|[session] variables;
	2.查看满足条件的部分系统变量
	show global|[session] variables like '%char%';
	3.查看指定的某个系统变量的值
	select @@global|[session].系统变量名;
	4.为某个系统变量赋值
	#法一：
	set global|[session]系统变量名 = 值;
	#法二：
	set @@global|[session].系统变量名 = 值;
*/
#1.全局变量
#①查看所有的全局变量
SHOW GLOBAL VARIABLES;
#②查看部分的全局变量
SHOW GLOBAL VARIABLES LIKE '%char%';
#③查看指定的某个系统变量的值
SELECT @@global.autocommit;
SELECT @@transaction_isolation;
#④为某个系统变量赋值
SET GLOBAL autocommit = 0;
SET @@global.autocommit = 1;


#2.会话变量
/*
作用域:仅仅针对当前会话(连接)有效

*/
#①查看所有的会话变量
SHOW VARIABLES;
#②查看部分的会话变量
SHOW VARIABLES LIKE '%char%';
#③查看指定的某个会话变量的值
SELECT @@session.transaction_isolation;
SELECT @@transaction_isolation;
#④为某个系统变量赋值
SET transaction_isolation = 'read-uncommitted';
SET @@session.transaction_isolation = 'REPEATABLE-READ';







#二、自定义变量
/*
说明:变量时用户自定义的，不是由系统规定好的
使用步骤: 声明 赋值 使用(查看、比较、运算等)
*/

#1.用户变量
/*
作用域:针对于当前会话(连接)有效,同于会话变量的作用域
可以应用在任何地方,也就是begin end里面或外面都可以
*/

#①声明并初始化
SET @用户变量名 = 值;
SET @用户变量名:=值;
SELECT @用户变量名:=值;
#②赋值(更新用户变量的值)
#方式一:通过set或select
	SET @用户变量名 = 值;
	SET @用户变量名:=值;
	SELECT @用户变量名:=值;
#方式二：通过select into
	SELECT 字段 INTO @变量名 FROM 表;

#③使用(查看用户变量的值)
SELECT @用户变量名;


#案例
USE myemployees;
#赋值
SET @name='john';
SET @name=100;
SET @count = 1;
SELECT COUNT(*) INTO @count FROM employees;
#使用
SELECT @count;

#2.局部变量
/*
作用域:仅仅在定义它的begin end 有效
应用在begin end中的第一句话
*/


#①声明
DECLARE 变量名 类型;
DECLARE 变量名 类型 DEFAULT 值;


#②赋值
#方式一:通过set或select
	SET 变量名 = 值;
	SET 变量名:=值;
	SELECT @局部变量名:=值;
#方式二：通过select into
	SELECT 字段 INTO 局部变量名 FROM 表;


#③使用
SELECT 局部变量名;


#对比用户变量、局部变量
		作用域	   	定义和使用的位置	  语法
#用户变量	当前会话	 会话中的任何地方 	必须加上@，不需限定类型
#局部变量	begin end中	begin end中且第一句话	一般不用加@ 除非通过select赋值,需要限定类型



#案例:声明两个变量并赋初始值，求和 打印

#1.用户变量
SET @m=1;
SET @n=2;
SET @sum = @m+@n;
SELECT @sum;

#2.局部变量
DECLARE m INT DEFAULT 1;
DECLARE n INT DEFAULT 2;
DECLARE SUM INT;
SET SUM = m+n;
SELECT SUM;










