#复习前一天的内容
/*
排序
	一、语法
		select 查询列表
		from 表名
		where 筛选条件
		group by 分组列表
		order by 排序列表[asc|desc]


	二、特点
		1.asc：升序，默认
		  desc：降序
		2.排序列表 支持 单个字段、多个字段、函数、表达式、别名

常见函数
	一、概述
		功能:类似方法
		特点:提高重用性，隐藏实现细节
		调用:select 函数名(实参列表);
	二、单行函数
		1.字符函数
			length:长度
			concat:连接
			substr:截取子串
			upper:变大写
			lower:变小写
			instr:获取索引位置
			trim:去前后空格
			lpad:左填充
			rpad:右填充
			replace:替换
		2.数学函数
			round:四舍五入
			mod:取余
			ceil:向上取整
			floor:向下取整
			truncate:截取
			rand:获取随机数，默认返回0-1之间的小数
		3.日期函数
			now:返回当前日期+时间
			year:年
			month:月
			day：日
			date_fromat:将日期转字符
			curdata:返回当前日期
			str_to_data:字符转日期
			curtime：返回当前时间
			hour:小时
			minute:分组
			second：秒
			datediff:返回两个日期相差的天数
			monthname:以英文形式返回月
		4.其他函数
			version:版本
			database:当前所在数据库
			user:当前用户
			md5('')：返回该字符的加密形式
		5.流程控制函数
			if(条件表达式,表达式1，表达式2):表达式成立返回1，否则返回2
			case情况1
				case 变量、表达式、字段
				when 常量 then 值
				.....
				else 值n
				end
			case情况2
				case 
				when 条件 then 值
				.....
				else 值n
				end
	三、分组函数
		1.分类
			max 最大值
			min 最小值
			sum 和
			count 计数
			avg 平均值
		2.特点
			语法 select max(字段) from 表名;
			支持的类型 sum avg 一般处理数值型
				   max min count 可以处理任何数据类型
		        以上分组函数都忽略null值
		        都可以搭配distinct使用，实现去重 select max(distinct 字段) from 表名
		        count函数
				count(字段): 统计该字段非空值的个数
				count(*)：统计结果集的行数
			和分组函数一同查询的字段，要求是group by后出现的字段
分组查询
	一、语法
		select 分组函数,分组后的字段 5
		from 表名 1
		where 筛选条件 2 
		group by 分组的字段 3 
		having 分组后的筛选 4 
		order by 排序列表 6
	二、特点
				常用关键字	筛选的表	位置
		分组前筛选	where		原始表		group by 前
		分组后筛选	having		分组后的结果	group by 后
连接查询
	一、含义
		当查询中涉及多个表字段
		select 查询到字段...
		from 查询涉及到的表1，表n...
		笛卡尔乘积：查询多个表，不添加有效连接条件，导致多个表所有行实现完全连接
		where 连接条件
	二、分类
		按年代:
			sql92
				等值
				非等值
				自连接
				
			sql99(推荐使用)
				内连接(等值 非等值 自连接)
				外连接(左外 右外 全外)
				交叉连接
	三、SQL92语法
		1.等值连接
			语法:
				select 查询列表
				from 表名1 别名1,表名2 别名2
				where 别名1.key = 别名2.key [and 筛选条件]
				group by 分组字段
				having 分组后的筛选条件
				order by 排序字段
			特点:
				1.一般起别名
				2.多表顺序可以调换
				3.n表连接，至少需要n-1个连接条件
				4.等值连接的结果是多表的交集部分
		2.非等值连接
			语法:
				select 查询列表
				from 表名1 别名1,表名2 别名2
				where 非等值连接条件
				group by 分组字段
				having 分组后的筛选条件
				order by 排序字段
		3.自连接
			语法:
				select 查询列表
				from 表名1 别名1,表名1 别名2
				where 别名1.key = 别名2.key [and 筛选条件]
				group by 分组字段
				having 分组后的筛选条件
				order by 排序字段
	四、SQL99语法
		1.内连接
		2.外连接
		3.交叉连接
			
		         
*/