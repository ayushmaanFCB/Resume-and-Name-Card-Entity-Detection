from pymongo.mongo_client import MongoClient
import re
from bson import ObjectId

uri = "mongodb+srv://ayushmaanFCB:ayonmongodb@cluster0.2uzsu2q.mongodb.net/?retryWrites=true&w=majority"

try:
    cluster = MongoClient(uri)
    db = cluster["NER_from_Documents_Project"]
    collection = db["Resumes"]
    print("\n\033[31mConnection to Database Successfull !!!\033[0m \n")
except Exception as e:
    print("Failed to connect to Mongo DB Database : ", e)


def pushToDB(post):
    result = collection.insert_one(post)
    return result


def searchFromDB(parameter, keyword):
    parameter = parameter.lower()
    if parameter in ["name", "email", "phone", "location"]:
        sub_cat = "basics"
    if parameter in ["position", "experience", "company"]:
        sub_cat = "work"
    if parameter in ["skill"]:
        sub_cat = "expertise"
    if parameter in ["certification"]:
        sub_cat = "achievements"
    if parameter != "id":
        results = collection.find(
            {"Key Points.{0}.{1}".format(sub_cat, parameter): re.compile(keyword, re.IGNORECASE)})
    if parameter == "id":
        results = collection.find(
            {"_id": ObjectId(keyword)})
    return results


def allRecords():
    return collection.find()
