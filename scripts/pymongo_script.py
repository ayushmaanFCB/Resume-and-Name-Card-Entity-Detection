from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ayushmaanFCB:ayonmongodb@cluster0.2uzsu2q.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["NER_from_Documents_Project"]
collection = db["Resumes"]

post1 = {"_id": 2, "name": "ABC"}
post2 = {"_id": 3, "name": "CDE"}

try:
    doc_counts = collection.count_documents({"count":25})
    print(doc_counts)
except Exception as e:
    print(e)
