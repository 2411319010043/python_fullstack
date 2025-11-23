use db_shop;
#用户表
CREATE TABLE IF NOT EXISTS USER(
	id INT PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(20) NOT NULL,
	email VARCHAR(100) DEFAULT NULL,
	phone INT DEFAULT NULL,
	age INT DEFAULT NULL
) ENGINE = innodb DEFAULT CHARSET = utf8;
ALTER TABLE user MODIFY COLUMN phone char(20) DEFAULT NULL;

#商品表
CREATE TABLE IF NOT EXISTS product(
	id INT PRIMARY KEY AUTO_INCREMENT,
	NAME VARCHAR(20) NOT NULL,
	price FLOAT(10,2) NOT NULL,
	stock INT NOT NULL,
	DESCRIPTION TEXT DEFAULT NULL
)ENGINE = innodb DEFAULT CHARSET = utf8;

alter table product modify column name char(50) not null;

#订单表
CREATE TABLE IF NOT EXISTS orders(
	id INT PRIMARY KEY AUTO_INCREMENT,
    user_id int not null,
	total_price decimal(10,2) not null,
	STATUS VARCHAR(20) not null, #订单的状态--已发货，未发货
	create_time TIMESTAMP not null DEFAULT CURRENT_TIMESTAMP,
	update_time TIMESTAMP not null DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
	order_date DATE,
    order_time time,
    shipping_address varchar(100) not null,
    payment_method varchar(50),#支付方式
    payment_status varchar(50), #支付状态--已支付，未支付
	FOREIGN KEY (user_id) REFERENCES USER(id)  on delete cascade #外键
)ENGINE = innodb DEFAULT CHARSET = utf8;
  

#创建orders和product的关联表
create table if not exists order_detial(
    id int PRIMARY key AUTO_INCREMENT,
    order_id int not null,
    product_id int not null,
    quantity INT not NULL,
    foreign key (order_id) references orders(id) on delete cascade,
    Foreign Key (product_id) REFERENCES product(id) on delete cascade

)engine = innodb default charset = utf8;