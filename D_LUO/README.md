# ddwang_book_sale
-- version 1       update time: 2019-12-31 --
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
