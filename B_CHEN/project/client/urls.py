"""C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

app_name = 'client'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('info/', views.info),
    path('info-post/', views.info_post),
    path('order/', views.order),
    path('return/', views.return_page),
    path('return_order/', views.return_order),
    path('confirm/', views.confirm),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('detail/<book_id>/', views.book_detail, name='book_detail'),
    path('addtocart/<book_id>/', views.addtocart, name='addtocart'),
]
