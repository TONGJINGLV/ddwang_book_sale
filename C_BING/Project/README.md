# ddwang_book_sale
-- version 2       update time: 2020-01-02 --
## 基本功能的设计-实现状况
* 查看购物车-购物车部分还未合并进来，所以此处查看的是最新一个订单的详情
* 购物车结算-获取用户填入的电话号码和收货地址信息，并生成订单（由于购物车部分还未合并进来，默认生成的订单为购买book_id=1、book_id=2的书各1本）
* 查看订单-用户可以查看订单
* 确认收货-订单生成后，用户可以选择确认收货
* 订单退货-订单生成后，用户可以选择退货
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
* 书店店主界面： http://127.0.0.1:8000/admin/
* Please log in with username "admin" and password "r00tpassw0rd"
* 用户购物车界面： http://127.0.0.1:8000/client/cart/
* Please log in with username "admin" and password "r00tpassw0rd"

