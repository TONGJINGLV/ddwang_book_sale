"""ddwang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from uauth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('changepassword/', views.changepassword),
    path('cart/', views.view_cart),
    path('view_cart/', views.view_cart, name='cart_detail'),
    path('home/', views.home, name='home'),
    path('search/', views.searchbooks, name='search'),
    path('home/search.html', views.searchbooks),
    path('index/search.html', views.searchbooks),
    path('detail/<book_id>/', views.book_detail, name='book_detail'),
    path('addtocart/<book_id>/', views.addtocart, name='addtocart'),
]
