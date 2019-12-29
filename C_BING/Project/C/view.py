from django.http import HttpResponse
from django.shortcuts import render
from bookstore import models

def cart(request):
	context = {}
	items = models.Book.objects.filter(bid__lt=10)
	context['heading'] = "购物车"
	context['content'] = "<div><ul>"
	for item in items:
		context['content'] += "<li>" + str(item.btitle) + "</li>"

	context['content'] += "</ul></div>"
	return render(request, 'hello.html', context)


def info(request):
	context = {}
	context['heading'] = "结算中心"
	context['content'] = "<form action=\"info-post/\" method=\"post\">收货地址<input type=\"text\" name=\"address\" />"
	context['content'] += "<br><input type=\"submit\" value=\"Submit\" /></form>"
	return render(request, 'hello.html', context)


def info_post(request):
	context = {}
	if request.POST:
		context['heading'] = "订单提交成功！"
		# request.POST['address']
		# create_order
		context['content'] = '正在跳转至订单详情页面...' + str(request.POST['address'])
	return render(request, 'hello.html', context)


def order(request):
	context = {}
	context['heading'] = "订单详情"

	# get the order details
	# orderid, ordertime, ordertype, ...

	context['content'] = "<div> </div>"
	return render(request, 'hello.html', context)

