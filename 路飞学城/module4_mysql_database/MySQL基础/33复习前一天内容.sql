#一、变量
/*
分类：1.系统变量：变量由系统提供
		全局变量：服务器层面的，必须拥有super权限才能为其赋值，作用域是整个服务器，也就是针对所有连接(会话)，重启的话所有配置都会失效
		会话变量：服务器为每一个连接的客户端提供的系统变量，作用域是当前连接
		
			①.查看系统变量
				show global|[session] variables;

			②.查看指定的系统变量的值
				select @@golbal|[session].变量名;
				show global|[session] variables like '';
			
			③.为系统变量赋值
				set global|[session] 变量名=值;
				set @@global.变量名 = 值;
				set @@变量名 = 值;
      2.自定义变量：变量是用户自己定义的
		用户变量：针对于当前连接(会话)生效
		
			①声明并赋值
				set @变量名 = 值;
				set @变量名 := 值;
				select @变量名 := 值;
			
			②更新值
				set @变量名 = 值;
				set @变量名 := 值;
				select @变量名 := 值;
				select 字段 into @变量名 from 表;
			
			③使用
				select @变量名;
		
		局部变量:仅仅在begin end中有效 只能放在begin end中的第一句
		
			①声明
				declare 变量名 类型 约束;
			
			②赋值或更新
				set 变量名 = 值;
				set 变量名 := 值;
				select @变量名 := 值;
				select 字段 into 变量名 from 表;
			
			③使用
				select 变量名;
			
		
			
*/

#二、存储过程和函数
/*
1.存储过程
	①创建
		create procedure 存储过程名( 参数模式 参数名 参数类型)
		begin
			存储过程体
		end
		
		注意：①参数模式：in(可省略) out inout
		      ②存储过程体的每一句SQL语句都需要用分号结尾
	②调用
		call 存储过程名(实参列表)
		调用in模式的参数: call sp1('');
		调用out模式的参数: set @name; call sp1(@name); select @name;
		调用inout模式的参数: set @name = 值; call sp1(@name); select @name;

	③查看
		show create procedure 存储过程名;
	④删除
		drop procedure 存储过程名;


2.函数
	①创建
		create function 函数名( 参数名 参数类型) returns 返回类型
		begin
			函数体
			return 返回值;
		end
		
		注意：①函数一定要有一个返回值

	②调用
		select 函数名(实参列表);

	③查看
		show create function 函数名;
	④删除
		drop function 函数名;


*/

#三、流程控制结构
/*
顺序结构:程序从上往下依次执行
分支结构:程序按条件选择执行
循环结构:程序满足一定条件下，重复执行一组语句
*/
#1.分支结构
/*
特点:

1.if函数；实现简单的双分支
	语法:
		if(条件，值1，值2);
	位置:可以作为表达式放在任何位置

2.case结构：实现多分支
	语法:
	case 表达式或字段
	when 要判断的值 then 表达式|语句;
	...
	else 语句n
	end [case];

3.if结构:只能放在begin end中
	语法：
		if 条件1 then 语句1;
		elseif 条件2 then 语句2;
		.....
		else 语句n;
		end if;
	
		
*/

#2.循环结构:都只能放在begin end中
/*
①.while
	语法: [名称:]while 条件 do
			循环体;
		end while [名称];
②.loop
	语法: [名称:] loop
			循环体;
		end loop [名称];
③.repeat
	语法: [名称:] repeat
			循环体;
		until 结束条件;
		end repeat [名称];	
		
		
④对比
	这三种循环都可以省略名称，但如果添加leave或iterate则必须添加名称
	loop 一般用于实现简单的死循环
	while 先判断后执行
	repeat先执行后判断

⑤循环控制语句
	leave:类似break 跳出所在循环
	iterate:类似continue 结束本次循环，继续下一次
	
*/













