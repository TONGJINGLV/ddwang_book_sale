# ddwang_book_sale
-- version 1       update time: 2019-12-31 --
## 注意ATTENTION尚未实现，需要在client添加的约束
* 退货订单生成前检查该客户已经购买过该数量的该商品
* 购买订单生成前检查书籍当时的状态是否on sale
## 基本功能的设计-实现状况
* 书店登录-书店全权限登录
* 书店进货记录-书店进货并自动更新库存
* 书店查看并处理客户订单（购买和退货）-书店查看订单并进行“确认发货"操作或者”确认收货“操作，并自动更新库存
* 库存查看-库存查看，并能自动检查库存是否与历史订单和进货记录统一
* 书籍上下架-书籍上下架，并能自动下架售罄的书籍
## 部署过程
### django: running the following command in a shell prompt:
```
python -m django --version
```
If Django is installed, you should see the version of your installation. If it isn’t, you’ll get an error telling “No module named django”, and please [install django](https://docs.djangoproject.com/en/3.0/intro/install/)
### copy all the project file to one directory
### migrate
* in the directory running the following command
```
python manage.py makemigrations
python manage.py migrate
```
### 运行服务器
run the following commands:
```
py manage.py runserver
```
### 使用服务
* Starting development server at http://127.0.0.1:8000/admin/
* Please log in with username "admin" and password "r00tpassw0rd"

## 逻辑结构设计：请阅读 /bookstore/models.py代码及注释
## 数据生成指南：
* 基本信息录入：先录入book（此时库存只能为默认的0）, supplier, customer, bookstore的数据；
* 进货：录入purchaseorder的数据，使得这些书目库存非0；
* 上架：在book表中修改on_sale，使书籍上架；
* 下单：此时前端client可正常下单；
* 发货：回到admin修改sendtime.
## 给前端在事务处理上的建议
* 把view操作打包成一个个事务，利用django的事务并行调度来提高可用性：https://docs.djangoproject.com/en/3.0/ref/settings/#atomic-requests
