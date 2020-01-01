# ddwang_book_sale
* 用户面对的登录与搜索网页，详见UI设计

* 嵌入django(clients app)

  ## 首页

  显示搜索框，登入键和所有书的书名和作者，点击书名进入该书详情页

![image](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101204439593.png)

## 登录页面

![image](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101204704913.png)

## 注册页面

![image](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101204758295.png)

## 修改密码页面

![image-20200101204833066](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101204833066.png)

## 登录后页面

![image-20200101204909445](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101204909445.png)

## 购物车页面

暂无

## 搜索结果页面

![image-20200101205021960](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101205021960.png)

## 加入购物车

![image-20200101205049278](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101205049278.png)

## 问题

加入购物车视图函数addtocart如下：

```python
def addtocart(request, book_id):
    username = request.session['user_name']
    cur_user = models.Customer.objects.get(cname=username)
    cur_book = models.Book.objects.get(book_id=book_id)

    item = {
        'book_id': cur_book.book_id,
        'title': cur_book.title,
        'quantity': 1,
        'price': cur_book.price
    }

    if cur_user:
        usession = cur_user.session

        if usession:
            cart = json.loads(usession)
        else:
            cart = {}
        if cur_book.book_id not in cart.keys():
            cart[cur_book.book_id] = item
        else:
            cart[cur_book.book_id]['quantity'] += 1

        cart_string = json.dumps(cart)
        cur_user.session = cart_string
        cur_user.is_active = True
        cur_user.last_active_time = datetime.now()
        cur_user.save()
        cur_user.refresh_from_db()
        return render(request, 'add_success.html')
    return render(request, 'index.html')
```

即使加入了百年孤独这本书，仍然进入以下条件分支

if cur_book.book_id not in cart.keys():
            cart[cur_book.book_id] = item

usession如下：

![image-20200101205516944](https://github.com/TONGJINGLV/ddwang_book_sale/blob/master/B_CHEN/images/image-20200101205516944.png)
