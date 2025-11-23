#常见的数据类型
/*

数值型:
	整型
	小数:
		定点数
		浮点数
字符型：
	较短的文本 char、varchar
	较长的文本 text、blob(较长的二进制数据)
日期型

*/



#一、整型
/*
分类:
	tinyint、smallint、mediumint、int/integer、bigint
	   1	     2	  	3	    4	      8
特点:
	1.如果不设置有无符合，默认有符号，设置无符号追加unsigned
	2.如果插入的数值超出了整型的范围 会报错
	3.如果不设置长度会有默认值
	4.长度代表显示的最大宽度，若不够会用0在左边填充，必须搭配zerofill使用
*/


#1.如何设置无符号和有符号
DROP TABLE IF EXISTS tab_int;
CREATE TABLE tab_int(
	t1 INT(7) ZEROFILL,#宽度 设置宽度搭配zerofill才会生效 一旦使用就只能无符号
	t2 INT UNSIGNED
);


DESC tab_int;

INSERT INTO tab_int SET t1 = -2; #默认有符号
INSERT INTO tab_int VALUES(-2,-22); #错误插入 报错

INSERT INTO tab_int VALUES(1,22);#验证宽度设定
SELECT * FROM tab_int;







#二、小数
/*
分类:
	1.浮点型
		float(M,D)
		double(M,D)
	2.定点型
		dec(M,D)
		decimal(M,D)
特点:
	①M和D： 可省略 但decimal省略的话 只能插入整数(10)部分 小数(0)部分插入不进去
		M 代表整数部分+小数部分的总长度 超过范围报错
		D 小数点保留D位 不够0填充
	②定点型的精度较高，如果要求插入数值精度较高如货币运算等可考虑使用
*/


#测试M和D
DROP TABLE IF EXISTS tab_float;
CREATE TABLE tab_float(
	f1 FLOAT,
	f2 DOUBLE,
	f3 DECIMAL
);

DESC tab_float;

INSERT INTO tab_float VALUES(123.222,123.22222,323.222222);

INSERT INTO tab_float VALUES(123.56,123.456,234.456);

INSERT INTO tab_float VALUES(1523.56,1523.456,2534.456);#输入的超过规定的最大长度，报错

SELECT * FROM tab_float;






#三、字符型

/*

较短的文本 char、varchar

较长的文本 text、blob(较长的二进制数据)

其他:
	binary和varbinary用于保存较短的二进制
	enum用于保存枚举
	set用于保存集合
	
特点:
	写法		M的含义		    		    特点          空间耗费	效率
	char(M)	      最大字符数(可以省略，默认1)	固定的字符数	   耗费高	 高
	varchar(M)    最大字符数(不可以省略)		可变的字符数	   耗费低        低
	
*/


DROP TABLES IF EXISTS tab_char;
CREATE TABLE tab_char(   #枚举类型 只能插入你设定的其中的值
	c1 ENUM('a','b','c')
);

INSERT INTO tab_char VALUES('a');
INSERT INTO tab_char VALUES('b');
INSERT INTO tab_char VALUES('c');
INSERT INTO tab_char VALUES('d'); # 错误直接忽略掉
INSERT INTO tab_char VALUES('a');

SELECT * FROM tab_char;

CREATE TABLE tab_set(s1 SET('a','b','c'));

INSERT INTO tab_set VALUES('b');
INSERT INTO tab_set VALUES('a,b');
INSERT INTO tab_set VALUES('a,c,d'); 
INSERT INTO tab_set VALUES('d,a,c,b');
INSERT INTO tab_set VALUES('b,a,c');


SELECT * FROM tab_set;


#四、日期型

/*
分类:
	date 保存日期
	time 保存时间
	year 保存年
	
	datetime 保存日期+时间
	timestamp 保存日期+时间
	
特点:
			字节	范围	时区等的影响
	datetime	  8   1000-9999	   不受
	tiemstamp	  4   1970-2038	    受

*/

DROP TABLES IF EXISTS tab_date;
CREATE TABLE tab_date(   
	t1 DATETIME,
	t2 TIMESTAMP
);

INSERT INTO tab_date VALUES(NOW(),NOW());

DESC tab_date;
SELECT * FROM tab_date;










