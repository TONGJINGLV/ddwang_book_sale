import hashlib

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from datetime import datetime

from . import forms
from . import models

import json
# Create your views here.
from .forms import UserForm
from .models import Customer


def index(request):
    book_list = models.Book.objects.all()
    if request.session.get('is_login', None):
        return redirect('/home/')
    return render(request, 'index.html', {'book_list': book_list})

def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.Customer.objects.get(cname=username)
            except:
                messages.error(request, '用户不存在！')
                return render(request, 'login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_tel'] = user.ctel
                request.session['user_name'] = user.cname
                messages.success(request, '登录成功')
                return redirect('/home/')

            else:
                messages.error(request, '密码错误！')
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/home/')

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
                return render(request, 'register.html', locals())
            if len(password1) < 6 or len(password1) > 20:
                message = '密码长度必须大于等于6并小于等于20！'
                return render(request, 'register.html', locals())
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.Customer.objects.filter(cname=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())

                new_user = models.Customer()
                new_user.cname = username
                new_user.ctel = ctel
                new_user.password = password1
                new_user.save()
                messages.success(request, '注册成功')
                return redirect('/login/')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/index/")


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
                return render(request, 'changepassword.html', locals())
            if user.password == oldpassword:
                if len(newpassword1) < 6 or len(newpassword1) > 20:
                    message = '密码长度必须大于等于6并小于等于20！'
                    return render(request, 'changepassword.html', locals())
                if newpassword1 != newpassword2:
                    message = '两次输入的密码不同！'
                    return render(request, 'changepassword.html', locals())
                user.password = newpassword1
                user.save()
                return render(request, 'index.html', locals())
            else:
                message = '密码不正确！'
                return render(request, 'changepassword.html', locals())
        else:
            return render(request, 'login.html', locals())

    change_form = forms.ChangepasswordForm()
    return render(request, 'changepassword.html', locals())


"""class SearchView(ListView):
    template_name = 'search.html'
    model = models.Book

    def get_queryset(self):
        try:
            name = self.kwargs['bookname']
        except:
            name = ''
        if name != '':
            object_list = self.model.objects.filter(title__icontains=name)
        else:
            object_list = self.model.objects.all()
        return object_list"""


def searchbooks(request):
    if request.method == 'GET':
        query = request.GET.get('bookname')

        if query is not None:
            lookups = Q(title__icontains=query)

            results = models.Book.objects.filter(lookups).distinct()

            context = {'results': results}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')


def book_detail(request, book_id):
    cur_book = models.Book.objects.get(book_id=book_id)

    return render(request, 'detail.html', {'cur_book': cur_book})


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


def view_cart(request):
    username = request.session['user_name']
    cur_user = models.Customer.objects.get(cname=username)

    if cur_user:
        usession = cur_user.session
        if usession:
            cart = json.loads(usession)
            return HttpResponse(usession)
        else:
            cart = {}
            return HttpResponse("购物车为空")

