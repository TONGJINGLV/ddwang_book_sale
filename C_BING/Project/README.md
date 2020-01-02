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
* 同时打开两个界面，开始模拟电商购物流程：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/pages.png)  
1. 在用户购物车界面点击结算，进入用户信息收集页面，填入用户信息（联系电话应为11位数）：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/info.png)  
2. 填好信息后点击submit提交，等待3秒后进入订单详情页面，可以看到此订单的编号为22：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/order.png)  
3. 此时从书店店主界面进入Orders，可以看到订单列表中出现22号订单：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/orderlist.png)  
4. 点击其订单编号22，进入订单编辑页面，将sendtime置为当前时间【模拟商家发货】：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/changeorder.png)  
5. 点击最下方save，保存，发现此时22号订单状态由“not delivered yet”变为“goods on the way”:  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/neworderlist.png)  
6. 此时刷新用户订单界面，订单状态也由“not delivered yet”变为“goods on the way”:  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/new.png)  
7. 此时用户可以选择确认收货，确认收货后，用户界面上订单状态变为“closed”，按钮选项变为“我要退货”；书店店主界面上刷新页面，该订单状态也变为“closed”.    
8. 此时用户可以选择我要退货，选择我要退货后，用户界面上按钮选项变为“我已退款发货”；书店店主界面上刷新页面，订单列表中出现23号退款订单：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/returnorder.png)  
9. 此时，退货的人变为用户，用户可以在用户界面选择“我已退款发货”（表明退货已经发出）；书店店主界面上刷新页面，23号退款订单状态变为“goods on the way”:  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/returnorderlist.png)  
10. 从书店店主界面点击订单编号23，进入订单编辑界面，将closetime置为当前时间【模拟商家收到退货后在系统中确认】：  
![](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/C_BING/Project/img/closetime.png)  
11. 点击最下方save，保存，发现此时23号订单状态由“goods on the way”变为“closed”.
12. 回到用户界面上刷新页面，订单状态也变为“closed”，流程结束。
* B部分还没有添加进来，所以缺少物品选购界面，后续会在用户界面上添加一个返回按钮用于返回物品选购页面
