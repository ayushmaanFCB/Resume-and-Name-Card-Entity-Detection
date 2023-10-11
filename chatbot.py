from transformers import pipeline
import pandas as pd
from pymongo.mongo_client import MongoClient
import re
from bson import ObjectId
import gradio

from scripts.mongodb_connect import fetchAllRecords

prompt = pipeline("table-question-answering",
                  model="google/tapas-base-finetuned-wtq")


def generatePrompt(message, history):
    datas = fetchAllRecords()
    records = []
    for data in datas:
        applicant = {}
        id = data["_id"]
        try:
            name = data['Key Points']['basics']['name'][0]
        except:
            name = "N.A."
        phone = data['Key Points']['basics']['phone']
        email = data['Key Points']['basics']['email']
        languages = data['Key Points']['basics']['language']
        locations = data['Key Points']['basics']['location']
        urls = data['Key Points']['basics']['url']
        skills = data['Key Points']['expertise']['skill']
        companies = data['Key Points']['work']['company']
        positions = data['Key Points']['work']['position']
        experiences = data['Key Points']['work']['experience']
        roles = data['Key Points']['work']['role']

        applicant.update({"id": id})
        applicant.update({"name": name})
        applicant.update({"phone": ", ".join(map(str, phone))})
        applicant.update({"email": ", ".join(map(str, email))})
        applicant.update({"languages": ", ".join(map(str, languages))})
        applicant.update({"locations": ", ".join(map(str, locations))})
        applicant.update({"urls": ", ".join(map(str, urls))})
        applicant.update({"skills": ", ".join(map(str, skills))})
        applicant.update({"companies": ", ".join(map(str, companies))})
        applicant.update({"positions": ", ".join(map(str, positions))})
        applicant.update({"experiences": ", ".join(map(str, experiences))})
        applicant.update({"roles": ", ".join(map(str, roles))})
        records.append(applicant)

        df = pd.DataFrame(records)
        df = df.astype(str)

    reply = prompt(table=df, query=message)["answer"]
    if reply == None or reply == "":
        return ("Sorry, I don't have the adequate information :(")
    else:
        return reply


chat = gradio.ChatInterface(theme=gradio.themes.Monochrome(),
                            fn=generatePrompt, title="Ask the Bot", submit_btn="SEND", autofocus=True)
