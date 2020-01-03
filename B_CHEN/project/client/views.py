from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators import csrf
from datetime import datetime
from bookstore import models
from django.db.models import Q
import json
from django.http import HttpResponse
from client import forms


def index(request):
    context = {}
    context['content'] = models.Book.objects.all()
    context['heading'] = 'ddwang'
    if request.session.get('is_login', None):
        return render(request, "client/home.html", context)
    return render(request, 'client/index.html', context)


def home(request):
    context = {}
    context['content'] = models.Book.objects.all()
    return render(request, 'client/home.html', context)


def book_detail(request, book_id):
    cur_book = models.Book.objects.get(book_id=book_id)
    assert isinstance(cur_book, object)
    context = {'cur_book': cur_book}
    return render(request, 'client/bookdetail.html', context)


def search(request):
    if request.method == 'GET':
        query = request.GET.get('bookname')

        if query is not None:
            lookups = Q(title__icontains=query)

            results = models.Book.objects.filter(lookups).distinct()

            context = {'results': results}

            return render(request, 'client/search.html', context)

        else:
            return render(request, "client/search.html")

    else:
        return render(request, 'client/search.html')


def register(request):
    if request.session.get('is_login', None):
        return redirect("client:home")

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            ctel = register_form.cleaned_data.get('ctel')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')

            if len(username) < 2 or len(username) > 25:
                message = '用户名字符长度必须大于等于2并小于等于25！'
                return render(request, 'client/register.html', locals())
            if len(password1) < 6 or len(password1) > 20:
                message = '密码长度必须大于等于6并小于等于20！'
                return render(request, 'client/register.html', locals())
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'client/register.html', locals())
            else:
                same_name_user = models.Customer.objects.filter(cname=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'client/register.html', locals())

                new_user = models.Customer()
                new_user.cname = username
                new_user.ctel = ctel
                new_user.password = password1
                new_user.save()
                # messages.success(request, '注册成功')
                return redirect("client:login")
        else:
            return render(request, 'client/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, "client/register.html", locals())


def login(request):
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.Customer.objects.get(cname=username)
            except:
                # messages.error(request, '用户不存在！')
                return render(request, 'client/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_tel'] = user.ctel
                request.session['user_name'] = user.cname
                request.session.set_expiry(60 * 30)  # 30min
                # messages.success(request, '登录成功')
                return redirect("client:home")

            else:
                # messages.error(request, '密码错误！')
                return render(request, 'client/login.html', locals())
        else:
            return render(request, 'client/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'client/login.html', locals())


def logout(request):
    context = {}
    context['content'] = models.Book.objects.all()
    context['heading'] = 'ddwang'
    if not request.session.get('is_login', None):
        return redirect("index")

    request.session.flush()
    # del request.session['is_login']
    return redirect("index")


def changepassword(request):
    if request.method == 'POST':
        change_form = forms.ChangepasswordForm(request.POST)
        message = ''
        if change_form.is_valid():
            username = change_form.cleaned_data.get('username')
            oldpassword = change_form.cleaned_data.get('oldpassword')
            newpassword1 = change_form.cleaned_data.get('newpassword1')
            newpassword2 = change_form.cleaned_data.get('newpassword2')

            try:
                user = models.Customer.objects.get(cname=username)
            except:
                message = '用户不存在！'
                return render(request, 'client/changepassword.html', locals())
            if user.password == oldpassword:
                if len(newpassword1) < 6 or len(newpassword1) > 20:
                    message = '密码长度必须大于等于6并小于等于20！'
                    return render(request, 'client/changepassword.html', locals())
                if newpassword1 != newpassword2:
                    message = '两次输入的密码不同！'
                    return render(request, 'client/changepassword.html', locals())
                user.password = newpassword1
                user.save()
                return redirect("index")
            else:
                message = '密码不正确！'
                return render(request, 'client/changepassword.html', locals())
        else:
            return redirect("client:login")

    change_form = forms.ChangepasswordForm()
    return render(request, 'client/changepassword.html', locals())


# @login_required(login_url='/login/', redirect_field_name='next')
def addtocart(request, book_id):
    if 'user_name' not in request.session.keys():
        form = forms.UserForm()
        context = {}
        context['login_form'] = form
        return render(request, "client/login.html", context)

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
        # return HttpResponse(usession)
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

        return HttpResponse("added successfully!")
        # return render(request, 'add_success.html')
    return render(request, 'client/index.html')


def cart(request):
    username = request.session['user_name']
    cur_user = models.Customer.objects.get(cname=username)
    if cur_user:
        usession = cur_user.session
        if usession:
            cart = json.loads(usession)
        else:
            cart = {}
            return HttpResponse("购物车为空")

    context = {}
    # items应改为购物车中的内容
    order_id = order_id = models.Order.objects.last().oid
    # items = models.Orderdetail.objects.filter(order=order_id)
    items = cart
    # items = models.Orderdetail.objects.filter(book_id__lt=2)
    context['heading'] = "购物车"
    context['content'] = items
    context['total'] = models.Order.objects.last().order_amount()
    context['buttons'] = "<button><a href=\"/client/info\">结算</a></button>"
    return render(request, 'client/cart.html', context)


def info(request):
    context = {}
    context['heading'] = "结算中心"
    return render(request, 'client/info.html', context)


def info_post(request):
    context = {}
    if request.POST:
        context['heading'] = "订单提交成功！"
        # request.POST['address']
        context['content'] = '还有<span id=\"countdown\">3</span>秒跳转至订单详情页面...'

        # get the infomation from the current cart
        cus = models.Customer.objects.get(cname='xz')
        items = [1, 2]

        # insert order information into the database
        models.Order.objects.create(customer=cus, order_time=datetime.now(), address=request.POST['address'],
                                    ctel=request.POST['tel'])
        # insert order_detail information into the database
        oid = models.Order.objects.last().oid
        for item in items:
            bid = item
            q = 1
            models.Orderdetail.objects.create(order_id=oid, book_id=bid, quantity=q)
    return render(request, 'client/pageJump.html', context)


def order(request):
    context = {}
    context['heading'] = "订单详情"

    # get the order details
    order_data = models.Order.objects.last()
    order_id = order_data.oid
    order_detail = models.Orderdetail.objects.filter(order=order_id)

    context['content'] = order_detail
    context['total'] = order_data.order_amount()
    context['detail'] = order_data

    if order_data.type == 'Y' and order_data.the_state_of_order() != 'closed':
        context['buttons'] = "<button><a href=\"/client/confirm\">确认收货</a></button>"
        if order_data.the_state_of_order() != 'goods on the way':
            context['buttons'] += "<button><a href=\"/client/return\">我要退货</a></button>"

    return render(request, 'client/cart.html', context)


def return_page(request):
    context = {}
    context['heading'] = "退款订单详情"

    # get the order details
    order_data = models.Order.objects.last()
    order_id = order_data.oid
    order_detail = models.Orderdetail.objects.filter(order=order_id)

    context['content'] = order_detail
    context['total'] = order_data.order_amount()
    context['detail'] = order_data

    # if the user wants to return the books before they're delivered, set the sendtime and closetime of the current order
    if order_data.the_state_of_order() == 'not delivered yet':
        order_data.sendtime = datetime.now()
        order_data.closetime = datetime.now()
        order_data.save()
        return render(request, "client/cart.html", context)
    else:  # otherwise, create a return order
        cus = models.Customer.objects.get(cname='xz')
        models.Order.objects.create(customer=cus, order_time=datetime.now(), type='N')
        new_order_id = models.Order.objects.last().oid
        for item in order_detail:
            models.Orderdetail.objects.create(order_id=new_order_id, book_id=item.book_id, quantity=item.quantity)

        context['buttons'] = "<button><a href=\"/client/return_order\">我已退款发货</a></button>"

    return render(request, "client/cart.html", context)


def return_order(request):
    context = {}
    context['heading'] = "退款订单详情"

    # get the order details
    order_data = models.Order.objects.last()
    order_data.sendtime = datetime.now()
    order_data.save()
    order_id = order_data.oid
    order_detail = models.Orderdetail.objects.filter(order=order_id)

    context['content'] = order_detail
    context['total'] = order_data.order_amount()
    context['detail'] = order_data

    return render(request, 'client/cart.html', context)


def confirm(request):
    context = {}
    context['heading'] = "订单详情"

    # get the order details
    order_data = models.Order.objects.last()
    order_data.closetime = datetime.now()
    order_data.save()
    order_id = order_data.oid
    order_detail = models.Orderdetail.objects.filter(order=order_id)

    context['content'] = order_detail
    context['total'] = order_data.order_amount()
    context['detail'] = models.Order.objects.last()

    context['buttons'] = "<button><a href=\"/client/return\">我要退货</a></button>"
    return render(request, "client/cart.html", context)
