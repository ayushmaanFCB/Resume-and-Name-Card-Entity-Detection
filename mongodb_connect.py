from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ayushmaanFCB:ayonmongodb@cluster0.2uzsu2q.mongodb.net/?retryWrites=true&w=majority"

try:
    cluster = MongoClient(uri)
    db = cluster["NER_from_Documents_Project"]
    collection = db["Resumes"]
except Exception as e:
    print("Failed to connect to Mongo DB Database : ", e)


def pushToDB(post):
    collection.insert_one(post)
