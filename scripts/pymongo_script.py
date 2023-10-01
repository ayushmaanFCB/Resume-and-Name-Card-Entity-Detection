from pymongo.mongo_client import MongoClient
import re

uri = "mongodb+srv://ayushmaanFCB:ayonmongodb@cluster0.2uzsu2q.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["NER_from_Documents_Project"]
collection = db["Resumes"]

post1 = {"_id": 2, "name": "ABC"}
post2 = {"_id": 3, "name": "CDE"}

results = collection.find(
    {'Key Points.basics.location': re.compile('delhi', re.IGNORECASE)})

for result in results:
    print(result)
