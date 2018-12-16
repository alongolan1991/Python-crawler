from pymongo import MongoClient

# Connect to db
MONGODB_URI = 'mongodb://admin:123abc@ds147033.mlab.com:47033/movies'
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("movies")
user_records = db.Items



def pushRECORD(record):
    user_records.insert_one(record)



def updateRecord(id, updates):
    user_records.update_one({'movie_id': id}, {
                            '$set': updates}, upsert=False)


def getRECORD(id):
    record = user_records.find_one({"movie_id": id})
    return record


