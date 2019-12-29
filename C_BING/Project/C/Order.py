import time


STORE_ID = 0


def create_order(db, addr):
	"""
	Create the current order
	:param db: the database
	:return: the order number
	"""

	cur = db.cursor()

	# get the content of the shopping cart
	cart = cart.get_cart_content()
	cost = cart

	# get customer id
	cus_id = 0

	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	cur.execute("INSERT INTO Order_ " +
				"(order_time, store_id, customer_id, order_amount, order_type, order_closetime) " +
				"VALUES (?,?,?,?,?, 0, NULL)", (current_time, STORE_ID, cus_id, cost))
	cur.execute("INSERT INTO OrderDetail (odtid, oid, book_id, quantity) VALUES (?,?)", (sessionid, data))
	# odtid, oid, book_id, quantity
	db.commit()
	orderid = last_insert_id()
	return orderid


def get_order_details(db, oid):
	orderid = oid
	# get the details of the order whose id is orderid
	list
	return list


def finish_order(db, finish_time):
	# update the finish time of the order
	return 1