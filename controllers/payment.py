from flask import jsonify, request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from .blueprint import order
from .blueprint import payment
from .auth import check_login, redirect_to_signin_form, is_admin
from models.user import User
from models.order import Order
from models.payment import Payment
import requests, json

# 결제 요청 페이지 API
@payment.route('/request')
def request_payment():
	user = check_login()
	if not user:
		return redirect_to_signin_form()

	order_id = request.args.get('order_id')
	order = Order.find_one(order_id)
	
	return render_template('payment.html', order=order)

# 결제 완료 및 주문상태 업데이트 API
@payment.route('/complete', methods=['POST'])
def complete_payment():
	user = check_login()
	if not user:
		return redirect_to_signin_form()
	
	request_data = request.get_json()
	imp_uid = request_data['imp_uid']
	merchant_uid = request_data['merchant_uid']

	# 결제가 정상적으로 완료되었는지 확인
	IAMPORT_GET_TOKEN_URL = 'https://api.iamport.kr/users/getToken'
	data = {
		"imp_key": "8426507666130745",
		"imp_secret": "KOUGO0bb2Pfh6iLBagBkDa98Kgz5aL4p5XOdzMlPRdqSrr9LA1C4BhSr2OuHB8wjUxQBhu3u12vZX1yN"
	}
	headers = {'Content-Type': 'application/json'}
	res = requests.post(IAMPORT_GET_TOKEN_URL, headers=headers, data=json.dumps(data))
	res = res.json()
	access_token = res['response']['access_token']

	iamport_get_payment_data_url = f'https://api.iamport.kr/payments/{imp_uid}'
	headers = {'Authorization': access_token}

	res = requests.get(iamport_get_payment_data_url, headers=headers)
	res = res.json()
	payment_data = res['response']

	order = Order.find_one(merchant_uid)
	if not order:
		return jsonify({'message':'존재하지 않는 주문입니다.'})

	if payment_data and payment_data['amount'] == order['product']['price']:
		status = 'success'
		Payment.insert_one(order, payment_data, status)
	else:
		status = 'fail'
		Payment.insert_one(order, payment_data, status)
		return jsonify({'message':'비정상적인 결제입니다.'})

	# update
	status = {'status': 'complete'}
	Order.update_one(merchant_uid, status)

	return jsonify({'order_id': merchant_uid, 'message': 'success'})



@payment.route('/success')
def success():
	order_id = request.args.get('order_id')
	return render_template('payment_complete.html', order_id=order_id)
