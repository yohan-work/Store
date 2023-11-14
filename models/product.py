from bson import ObjectId
from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId


class Product():
	@staticmethod
	def insert_one(product, thumbnail_img_url, detail_img_url):
		db = conn_mongodb()
		db.products.insert_one({
			'name': product['name'],
			'price': int(product['price']),
			'description': product['description'],
			'thumbnail_img': thumbnail_img_url,
			'detail_img': detail_img_url,
			'user': 'admin',
			'created_at': int(datetime.now().timestamp()),
			'updated_at': int(datetime.now().timestamp())
		})


	@staticmethod
	def find():
		db = conn_mongodb()
		products = db.products.find({})

		return products


	@staticmethod
	def delete_one(id):
		db = conn_mongodb()
		db.products.delete_one({'_id': ObjectId(id)})


	@staticmethod
	def update_one(id, product, thumbnail_img_url, detail_img_url):
		db = conn_mongodb()

		new_product = {
			'name': product['name'],
			'price': int(product['price']),
			'description': product['description'],
			'user': 'admin',
			'updated_at': int(datetime.now().timestamp())
		}

		if thumbnail_img_url:
			new_product['thumbnail_img'] = thumbnail_img_url

		if detail_img_url:
			new_product['detail_img'] = detail_img_url

		db.products.update_one(
			{'_id' : ObjectId(id)},
			{'$set': new_product}
		)


	@staticmethod
	def find_one(id):
		db = conn_mongodb()
		product = db.products.find_one({'_id': ObjectId(id)})

		return product
