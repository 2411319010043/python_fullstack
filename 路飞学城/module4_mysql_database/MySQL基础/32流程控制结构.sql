#流程控制结构
/*
顺序结构：查询从上往下依次执行
分支结构：程序从两条或多条路径中选择一条去执行
循环结构：程序在满足一定条件的基础上，重复执行一段代码
*/

#一、分支结构
#1.if函数
/*
功能：实现简单的双分支
语法： if(表达式1，表达式2，表达式3)
执行顺序：1成立 返回2 否则返回3
*/
#2.case结构
/*


情况一：类似Java中的switch语句，用于等值判断
	语法：  case 变量|表达式|字段
		when 要判断的值  then 返回值1或语句1;
		when 要判断的值  then 返回值2或语句2;
		......
		else 要返回的值n或语句n;
		end|end case;
情况二：类似于Java中的多重if语句，用于区间判断
	语法：  case 
		when 要判断的条件1  then 返回值1或语句1;
		when 要判断的条件2  then 返回值2或语句2;
		......
		else 要返回的值n或语句n;
		end|end case;
	
		
特点：
①可以作为表达式，嵌套在其他语句中使用，可以放在任何地方，begin end 中或begin end的外面
 可以作为独立的语句去使用，只能放在 begin end中
②如果when中的值满足或条件成立，则执行对应的then后面的语句，并结束cese
  如果都不满足，则执行else中的语句或值
③else可以省略，如果else省略了，且所有when条件都不满足，则返回null

*/

#案例
#创建存储过程，根据传入的成绩，显示等级
#90-100显示A , 80-90显示B, 60-80显示C，否则显示D
DELIMITER $
CREATE PROCEDURE test_case(IN score INT)
BEGIN
	CASE
	WHEN score BETWEEN 90 AND 100 THEN SELECT 'A';
	WHEN score BETWEEN 80 AND 89 THEN SELECT 'B';
	WHEN score BETWEEN 60 AND 79 THEN SELECT 'C';
	ELSE SELECT 'D';
	END CASE;

END$

CALL test_case(99)$


#3.if结构
/*
功能：实现多重分支
语法：if 条件1 then 语句1;
      elseif 条件2 then 语句2;
      ...
      [else 语句n;]
      end if;
应用在begin end中
*/

#案例 创建存储过程，根据传入的成绩，返回等级
#90-100返回A , 80-90返回B, 60-80返回C，否则返回D
CREATE FUNCTION test_if(score INT) RETURNS VARCHAR(2)
BEGIN
	DECLARE g VARCHAR(2);
	IF score BETWEEN 90 AND 100 THEN SET g='a';
	ELSEIF score BETWEEN 80 AND 89 THEN SET g='b';
	ELSEIF score BETWEEN 60 AND 79 THEN SET g='c';
	ELSE SET g='d';
	END IF;
	RETURN g;
END$

SELECT test_if(50)$




#二、循环结构
/*
分类：while、loop、repeat
循环控制：iterate(continue)、leave(break)
*/
#1.while
/*
语法：
	[标签:] while 循环条件 do
		循环体;
	end while [标签];
*/

#2.loop
/*
语法：
	[标签:] loop
		循环体;
	end loop [标签];
可以用来模拟简单的死循环
*/

#3.repeat
/*
语法：
	[标签:] repeat
		循环体;
	until 结束循环的条件
	end repeat [标签];

*/


#案例 没有添加循环控制语句
#批量插入，根据设置的次数倒admin表中的记录
CREATE PROCEDURE pro_while1(IN insertCount INT)
BEGIN
	DECLARE i INT DEFAULT 1;
	WHILE i <= insertCount DO
		INSERT INTO ADMIN(username,`password`) VALUES(CONCAT('richal',i),00000);
		SET i = i +1;
	END WHILE;
 
END$

CALL pro_while1(2)$

#案例 添加leave语句
#批量插入，根据设置的次数倒admin表中的记录 如果次数大于20 则停止
TRUNCATE TABLE `admin`;
CREATE PROCEDURE pro_while2(IN insertCount INT)
BEGIN
	DECLARE i INT DEFAULT 1;
	a:WHILE i <= insertCount DO
		INSERT INTO ADMIN(username,`password`) VALUES(CONCAT('小花',i),00000);
		IF i >= 20 THEN LEAVE a;
		END IF;
		SET i = i +1;

	END WHILE a;
 
END$

CALL pro_while2(30)$

#案例 添加iterate语句
#批量插入，根据设置的次数倒admin表中的记录 只插入偶数次
TRUNCATE TABLE `admin`;
CREATE PROCEDURE pro_while3(IN insertCount INT)
BEGIN
	DECLARE i INT DEFAULT 0;
	a:WHILE i <= insertCount DO
		SET i = i +1;
		IF MOD(i,2) !=0 THEN 
			ITERATE a;
		END IF;
		INSERT INTO ADMIN(username,`password`) VALUES(CONCAT('小花',i),00000);


	END WHILE a;
 
END$

CALL pro_while3(30)$





#案例
/* 
已知表stringcontent
其中字段：
id 自增长
content varchar(20)
向该表中插入指定个数的随机的字符串
*/

CREATE TABLE stringcontent(
	id INT PRIMARY KEY AUTO_INCREMENT,
	content VARCHAR(26)
);
DELIMITER $
CREATE PROCEDURE test_randstr_insert(IN insertCount INT)
BEGIN
	DECLARE str VARCHAR(26) DEFAULT 'abcdefghijklmnopqrstuvwxyz';
	DECLARE i INT DEFAULT 1; 
	DECLARE startIndex INT DEFAULT 1;
	DECLARE len INT DEFAULT 1;
	WHILE i <= insertCount DO
		SET startIndex = FLOOR(RAND()*26 +1);#产生一个随机整数，代表起始索引0-26
		SET len = FLOOR(RAND()*(21-startIndex)+1);#1-(26-startIndex+1)
		#set len = floor(rand()*(26-startIndex+1)+1);
		INSERT INTO stringcontent(content) VALUES(SUBSTR(str,startIndex,len));
		SET i = i+1;
	END WHILE;
END$

CALL test_randstr_insert(3)$





















