from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId


class Payment():
	@staticmethod
	def insert_one(order, payment_data, status):
		db = conn_mongodb()
		db.payments.insert_one({
			'order': order,
			'payment_data': payment_data,
			'status': status
		})
