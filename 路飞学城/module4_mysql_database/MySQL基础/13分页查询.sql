#进阶8：分页查询
/*
应用场景:
	当显示的数据，一页显示不全，需要分页提交sql请求
语法:
	select 查询列表  7
	from 表    1
	[join type] join 表2  2
	on 连接条件  3
	where 筛选条件  4
	group by 分组字段  5
	having 分组后的筛选  6
	order by 排序  8
	limit offset,size; #要显示条目的起始索引(0开始),要显示的条目个数   9
	
特点:	limit语句在查询语句的最后，也是执行顺序的最后
	公式
		要显示的页数page,每页的条目数size
		page      offset                            size=10
		1          0      offset= (page-1)*size
		2          10     offset=  (2-1) *10
		3          20	  offset = (3-1)*10
		select 查询列表
		from 表
		limit 
*/

#查询前5条员工信息
SELECT * FROM `employees` LIMIT 0,5;
#从第一条开始可以省略
SELECT * FROM `employees` LIMIT 5;

#查询第11条到25条
SELECT * FROM `employees` LIMIT 10,15;

#查询有奖金的员工信息，且工资较高的前10名
SELECT * FROM `employees` WHERE `commission_pct` IS NOT NULL ORDER BY `salary` DESC LIMIT 10;














