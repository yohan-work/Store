from flask import request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from .blueprint import order
from .auth import check_login, redirect_to_signin_form, is_admin
from models.user import User
from models.order import Order

# 구매 완료한 주문 목록
@order.route('/list')
def get_orders():
	user = check_login()
	if not user:
		return redirect_to_signin_form()

	match = {'status' : 'complete'}
	orders = Order.find(match)
	return render_template('orders.html', orders=orders)


# 상세 페이지
@order.route('/<order_id>')
def detail(order_id):
	user = check_login()
	if not user:
		return redirect_to_signin_form()

	order = Order.find_one(order_id)
	return render_template('order.html', order=order)