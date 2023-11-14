from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId


class Order():
	@staticmethod
	def insert_one(product, form, user):
		db = conn_mongodb()
		new_order_doc = db.orders.insert_one({
			'status': 'pending',
			'product': product,
			'postcode': form['postcode'],
			'address': form['address'],
			'detail_address': form['detail_address'],
			'extra_address': form.get('extra_address', ''),
			'user_name': form['user_name'],
			'user_phone': form['user_phone'],
			'user': user,
			'created_at': int(datetime.now().timestamp()),
			'updated_at': int(datetime.now().timestamp()),
		})

		return new_order_doc.inserted_id


	def find(match={}):
		db = conn_mongodb()
		orders = db.orders.find(match)

		return orders


	def find_one(order_id):
		db = conn_mongodb()
		order = db.orders.find_one({'_id': ObjectId(order_id)})

		return order


	def update_one(order_id, status):
		db = conn_mongodb()
		db.orders.update_one({'_id': ObjectId(order_id)}, {'$set': status})
