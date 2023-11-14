from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from .blueprint import product
from .blueprint import payment
from .auth import is_admin, check_login, redirect_to_signin_form
from models.product import Product
from models.order import Order
from datetime import datetime
import os

########## 등록 ##########
# 상품 등록 페이지 API
@product.route('/form')
def form():
	if not is_admin():
		return redirect(url_for('product.get_products'))

	return render_template('product_form.html')

# 상품 등록 API
@product.route('/regist', methods=['POST'])
def regist():
	if not is_admin():
		return redirect(url_for('product.get_products'))

	# 전달받은 상품 정보
	form_data = request.form
	thumbnail_img = request.files.get('thumbnail_img')
	detail_img = request.files.get('detail_img')
	thumbnail_img_url = ""
	detail_img_url = ""

	if thumbnail_img:
		thumbnail_img_url = _upload_file(thumbnail_img)
	if detail_img:
		detail_img_url = _upload_file(detail_img)

	# 저장하는 일
	Product.insert_one(form_data, thumbnail_img_url, detail_img_url)
	return redirect(url_for('product.get_products'))

########## //등록 ##########


########## 조회 ##########

# 상품 리스트 조회 API
@product.route('/list')
def get_products():
	# 상품 리스트 정보 < mongo db > products > collection의 documents
	products = Product.find()

	return render_template('products.html', products=products)

	return "상품 리스트 조회 API"

########## //조회 ##########



########## 삭제 ##########

# 상품 삭제 API
@product.route('/<product_id>/delete')
def delete(product_id):
	if not is_admin():
		return redirect(url_for('product.get_products'))

	# 상품 삭제
	Product.delete_one(product_id)

	return redirect(url_for('product.get_products'))

########## //삭제 ##########


########## 수정 ##########

# 상품 정보 수정 페이지 API
@product.route('/<product_id>/edit')
def edit(product_id):
	if not is_admin():
		return redirect(url_for('product.get_products'))
	product = Product.find_one(product_id)

	return render_template('product_edit.html', product=product)

# 상품 정보 수정 API
@product.route('/<product_id>/update', methods=['post'])
def update(product_id):
	if not is_admin():
		return redirect(url_for('product.get_products'))

	form_data = request.form
	thumbnail_img = request.files.get('thumbnail_img')
	detail_img = request.files.get('detail_img')
	thumbnail_img_url = ""
	detail_img_url = ""

	if thumbnail_img:
		thumbnail_img_url = _upload_file(thumbnail_img)
	if detail_img:
		detail_img_url = _upload_file(detail_img)

	Product.update_one(product_id, form_data, thumbnail_img_url, detail_img_url)

	return redirect(url_for('product.get_products'))

########## //수정 ##########


########## 상품상세 ##########

# 상품 상세 정보 페이지 API
@product.route('<product_id>/detail')
def detail(product_id):
	product = Product.find_one(product_id)

	return render_template('product.html', product=product)


########## //상품상세 ##########



########## 주문 ##########

# 주문 페이지 API
@product.route('<product_id>/order')
def order_form(product_id):
	product = Product.find_one(product_id)

	return render_template('order_form.html', product=product)


# 주문 생성 API
@product.route('/<product_id>/order', methods=['POST'])
def order(product_id):
	user = check_login()
	if not user:
		return redirect_to_signin_form()

	product = Product.find_one(product_id)
	form_data = request.form

	order_id = Order.insert_one(product, form_data, user)

	return redirect(url_for('payment.request_payment', order_id=order_id))


########## //주문 ##########


def _upload_file(img_file):
	timestamp = str(datetime.now().timestamp())
	filename = timestamp + '_' + secure_filename(img_file.filename)
	image_path = f'./static/uploads'
	os.makedirs(image_path, exist_ok=True)
	img = os.path.join(image_path, filename)
	img_file.save(img)

	return f'/static/uploads/' + filename