from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators import csrf
from datetime import datetime
from bookstore import models


def cart(request):
	context = {}
	# items应改为购物车中的内容
	order_id = order_id = models.Order.objects.last().oid
	items = models.Orderdetail.objects.filter(order=order_id)

	# items = models.Orderdetail.objects.filter(book_id__lt=2)
	context['heading'] = "购物车"
	context['content'] = items
	context['total'] = models.Order.objects.last().order_amount()
	context['buttons'] = "<button><a href=\"/client/info\">结算</a></button>"
	return render(request, 'client/hello.html', context)


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
		items = [1,2]

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

	return render(request, 'client/hello.html', context)


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
		return render(request, "client/hello.html", context)
	else:  # otherwise, create a return order
		cus = models.Customer.objects.get(cname='xz')
		models.Order.objects.create(customer=cus, order_time=datetime.now(), type='N')
		new_order_id = models.Order.objects.last().oid
		for item in order_detail:
			models.Orderdetail.objects.create(order_id=new_order_id, book_id=item.book_id, quantity=item.quantity)

		context['buttons'] = "<button><a href=\"/client/return_order\">我已退款发货</a></button>"

	return render(request, "client/hello.html", context)


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

	return render(request, 'client/hello.html', context)


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
	return render(request, "client/hello.html", context)


