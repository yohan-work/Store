import pymongo

MONGO_URI = "mongodb+srv://yohanmanage:dlKd5dtxXxZrpbwI@cluster0.or0gno1.mongodb.net/?retryWrites=true&w=majority"
MONGO_CONN = pymongo.MongoClient(MONGO_URI)

def conn_mongodb():
	db = MONGO_CONN.online_store
	return db
