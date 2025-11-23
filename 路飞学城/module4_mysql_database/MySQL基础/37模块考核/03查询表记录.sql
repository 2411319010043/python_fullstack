use db_shop;

#1. 获取用户ID为5的订单的订单号和订单日期。
select orders.order_num,orders.order_date 
from orders 
where user_id = 5;

#2. 获取每个用户的订单数量，并按订单数量降序排序。
select user_id,count(*) as 订单数量 
from orders 
group by user_id 
order by 订单数量 desc;

#3. 获取订单id为10的订单的所有产品信息（产品名称、价格、数量）。
select order_id,name,price,quantity
from product 
join order_detial on product_id = product.id 
where order_id = 10;

#4. 获取用户ID为1的所有订单的订单号、订单日期和产品数量总和，并按产品数量排序。
select user_id,order_num,order_date,sum(quantity) as 总和
from orders 
join order_detial on orders.id = order_id
where user_id = 1 
group by user_id,order_num,order_date
order by 总和;

#5. 获取订单日期在2024年2月份的所有订单的订单号、订单日期和产品数量总和，并按产品数量排序。
select order_num,order_date,sum(order_detial.quantity) as 总和
from order_detial 
join orders on orders.id = order_id 
where  order_date BETWEEN '2024-02-01' and '2024-02-29'
group by order_num,order_date
order by 总和;

#6. 获取产品名称为"Samsung Galaxy S21"的所有订单的订单号和订单日期。
select name,order_date,order_num 
from orders 
join order_detial on orders.id = order_id 
join product on product_id = product.id 
where name = 'Samsung Galaxy S21';

#7. 获取订单中产品数量大于等于3的订单号和订单日期。
select order_num,order_date,sum(order_detial.quantity) as 总和 
from orders 
join order_detial on orders.id = order_id 
join product on product_id = product.id 
group by order_num,order_date 
having 总和 >= 3;

#8. 获取有产品价格在100到500之间的订单的订单号和订单日期。
select DISTINCT order_num,order_date ,price 
from orders 
join order_detial on orders.id = order_id 
join product on product_id = product.id 
where price between 100 and 500;

#9. 获取用户ID为4的订单中购买产品数量最多的产品名称、数量和价格。
select user_id,name,stock price 
from product 
join order_detial on product_id = product.id  
join orders on orders.id = order_id 
where user_id = 4;

#10. 获取订单中产品数量最多的订单号和产品数量。
select order_num,sum(order_detial.quantity) as 数量
from orders 
join order_detial on orders.id = order_id 
join product on product_id = product.id 
group by order_num
order by 数量 desc
limit 1;

#11. 获取产品价格最高的订单的订单号和产品价格。
select order_num,price 
from product 
join order_detial on product_id = product.id 
join orders on order_id = orders.id 
order by price desc
limit 1;

#12. 获取哪些订单的平均产品数量超过所有订单平均产品数量的订单的订单号和产品数量。
#单独订单平均产品数量 》 所有订单的平均产品数量

#每个订单的平均产生数量
select order_num,avg(quantity) c from orders join order_detial on orders.id = order_id
group by order_num; 

SELECT 
    orders.order_num,
    SUM(quantity) as 产品数量
FROM orders 
JOIN order_detial ON orders.id = order_id 
GROUP BY orders.order_num
HAVING SUM(quantity) / COUNT(*) > (
    SELECT AVG(平均数量) FROM (
        SELECT SUM(quantity) / COUNT(*) as 平均数量
        FROM order_detial
        GROUP BY order_id
    ) as 每个订单的平均值
);
























