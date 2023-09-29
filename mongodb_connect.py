from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ayushmaanFCB:ayonmongodb@cluster0.2uzsu2q.mongodb.net/?retryWrites=true&w=majority"

try:
    cluster = MongoClient(uri)
    db = cluster["NER_from_Documents_Project"]
    collection = db["Resumes"]
    print("\n\033[31mConnection to Database Successfull !!!\033[0m \n")
except Exception as e:
    print("Failed to connect to Mongo DB Database : ", e)


def pushToDB(post):
    collection.insert_one(post)


def searchFromDB(keyword):
    results = collection.find({"Key Points.expertise.skill": keyword})
    x = []
    for result in results:
        x.append(result)
    return x
