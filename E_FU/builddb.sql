-- NOTE --
-- Please change the path in load_date_infile query into your own path --
-- before copy all query into cmd or use source to excute this file. --

-- create db --
drop database ddwang;
create database ddwang;
use ddwang;



-- 建立书店表 --
create table bookstore(
	bsname varchar(255), -- 书店名 --
	bstel char(8) not null, -- 书店电话 --
	baddr varchar(255), -- 书店地址 --
	bosstel char(13), -- 老板电话 --
	bosspasswd varchar(255), -- 老板登录密码 --
	staffpasswd varchar(255) -- 员工登录密码 --
); 
-- DBA加载数据 --
insert into bookstore values('财富守护书店', '88888888', '广东省东莞市财富守护书店', '18888888888', '666', '111');



-- 建立供应商表 --
create table supplier(
	sid int auto_increment,-- 主键id，auto_increment的用法可以百度一下 --
	sname varchar(255), -- 供应商名称 --
	stel char(8) not null, -- 供应商电话 --
	scity varchar(31), -- 供应商城市 --
	sregtime datetime not null, -- 注册日期，datatime的格式是"year-month-day hour:minute:second“ --
	primary key(sid)
);
-- DBA加载数据 --
load data infile '/var/lib/mysql-files/supplier.csv' into table supplier fields terminated by ','( sname, stel, scity, sregtime ) set sid=null;



-- 建立用户表 --
create table customer(
	cname varchar(255), -- 客户名字 --
	ctel char(11) not null, -- 客户电话作为主键 --
	last_active_time datetime not null, -- 最近活跃时间 --
	password varchar(255) not null, -- 密码，只对用户可见 --
	primary key(ctel)
);
-- DBA加载数据 --
load data infile '/var/lib/mysql-files/user.csv' into table customer fields terminated by ',';



-- 建立书表 --
create table book(
	bid int auto_increment, -- 主键id --
	btitle varchar(255) not null,  -- 书名 --
	bauthor varchar(1023), -- 作者，存在多个作者的情况，储存为 author1|author2|author3|... --
	bedition varchar(1023), -- 出版社 --
	bformat varchar(127), -- 版型：hardcover、papercover这种 --
	bpages int, -- 页数 --
	brating float, -- 评分 --
	bratcount int, -- 评分人数 --
	brevcount int, -- 评论人数 --
	bgenres varchar(1023), -- 分类，存在多个分类的情况，储存为 genres1|genres2|genres3|... --
	primary key(bid)
);
-- DBA加载数据 --
load data infile '/var/lib/mysql-files/book.csv' into table book fields terminated by '`'( btitle, bauthor, bedition, bformat, @bpages,brating, bratcount,brevcount,bgenres) set bid=null,bpages=if(@bpages='',null,@bpages);



-- 上架书目表 --
create table Stock(
	book_id int not null, -- 书编号 --
	stock_quantity int not null, -- 存量 --
	outprice float not null, -- 售价 --
	foreign key(book_id) references book (bid)
);



-- 未上架书目表 --
create table Stock_notsale(
	book_id int not null, -- 书编号 --
	stock_quantity int not null, -- 存量 --
	outprice float not null, -- 售价 --
	foreign key(book_id) references book (bid)
);




-- 销售订单表 --
create table Order_(
	oid int auto_increment, -- 订单编号 --
	order_time datetime, -- 订单确认时间 --
	customer_tel char(11) not null, -- 客户电话 --
	order_amount float not null, -- 交易金额 --
	order_type bool not null, -- 订单类型，0表示购买订单，1表示退货订单 --
	order_closetime datetime, -- 订单完成时间，初始null，确认时update --
	primary key(oid),
	foreign key(customer_tel) references customer (ctel)
);



-- 订单详情表 --
create table OrderDetail(
	order_id int not null, -- 订单id --
	book_id int not null, -- 书id --
	quantity int not null, -- 数量 --
	price float not null, -- 单价 --
	primary key(order_id, book_id),
	foreign key(order_id) references Order_ (oid),
	foreign key(book_id) references book (bid)
);



-- 进货订单表 --
create table PurchaseOrder(
	poid int auto_increment, -- 订单id --
	porder_time datetime not null, -- 订单生成时间 --
	supplier_id int not null, -- 供应商id --
	porder_amount float not null, -- 交易金额 --
	porder_type bool not null, -- 订单类型，0表示购买订单，1表示退货订单 --
	porder_closetime datetime, -- 订单完成时间，初始null，确认时update --
	primary key(poid),
	foreign key(supplier_id) references supplier (sid)
);


-- 供应商订单详情表 --
create table PurchaseOrderDetail(
	porder_id int not null, -- 订单id --
	book_id int not null, -- 书本id --
	quantity int not null, -- 数量 --
	price float not null, -- 单价 --
	primary key(porder_id),
	foreign key(porder_id) references PurchaseOrder (poid),
	foreign key(book_id) references book (bid)
);
