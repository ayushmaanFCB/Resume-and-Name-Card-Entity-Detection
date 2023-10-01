import gradio
import re
from mongodb_connect import searchFromDB


def searchResumes(parameter, keyword):
    flag = False
    results = searchFromDB(parameter, keyword)
    output = """<div>"""
    for result in results:
        flag = True
        id = result["_id"]
        try:
            name = result['Key Points']['basics']['name'][0]
        except:
            name = "N.A."
        phone = result['Key Points']['basics']['phone']
        email = result['Key Points']['basics']['email']
        languages = result['Key Points']['basics']['language']
        locations = result['Key Points']['basics']['location']
        urls = result['Key Points']['basics']['url']
        skills = result['Key Points']['expertise']['skill']
        companies = result['Key Points']['work']['company']
        positions = result['Key Points']['work']['position']

        phone, email, languages, locations = [
            "-" if not data else data for data in (phone, email, languages, locations)]
        output = output + \
            """<h1 style='text-align:center'>{0}</h1> <table style='margin-right:auto; margin-left:auto'><tr><th>ID</th><th>CONTACT NUMBER</th><th>EMAIL IDs</th><th>LOCATIONS</th><th>LANGUAGES</th></tr>""".format(
                name.upper())
        output = output + """<tr><tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>""".format(
            id, ", ".join(map(str, phone)), ", ".join(map(str, email)), ", ".join(
                map(str, locations)), ", ".join(map(str, languages))
        )
        output = output + "</table>"

        datas = [companies, positions, skills, urls]
        messages = ["</table><h2>Companies worked at : </h2>", "</table><h2>Job Designations / Positions : </h2>",
                    "</table><h2>Applicant Skillset : </h2>", "</table><h2>Profile reference links : </h2>"]
        for i, data in enumerate(datas):
            if data != []:
                output = output + "<h2>{0}</h2>".format(messages[i])
                for info in data:
                    output = output + \
                        "<span style='margin-right: 20px'>{0}</span>".format(
                            info)

    if flag == False:
        output = """<h1 style='color:red'>Sorry, No such record exists in the database</h1>"""

    output = output + "</div>"
    return output


def searchByParameters(parameter, keyword):
    flag = False
    results = searchFromDB(parameter, keyword)
    output = """<div>"""
    for result in results:
        flag = True
        id = result["_id"]
        name = result['Key Points']['basics']['name'][0]
        phone = result['Key Points']['basics']['phone']
        email = result['Key Points']['basics']['email']


with gradio.Blocks() as block:
    with gradio.Row():
        gradio.HTML("<h1 style='text-align:center'>DATABASE QUERYING<h1>")

    with gradio.Tab(label="SEARCH FOR UPLOADED RESUMES") as tab1:
        with gradio.Row():
            with gradio.Column(scale=4):
                parameter = gradio.Radio(label="SELECT THE PARAMETER YOU WANT TO SEARCH USING",
                                         choices=["ID", "NAME", "EMAIL", "PHONE"], value="NAME")
                keyword = gradio.Text(label="ENTER THE SEARCH DATA")
            with gradio.Row():
                submit = gradio.Button(value="SEARCH THE DATABASE")
        with gradio.Row():
            submit.click(fn=searchResumes, inputs=[
                parameter, keyword], outputs=[gradio.HTML()])

    with gradio.Tab(label="SEARCH USING TERMS") as tab1:
        with gradio.Row():
            with gradio.Column(scale=4):
                parameter = gradio.Dropdown(label="WHAT DO YOU WANT TO SEARCH USING ?",
                                            choices=["SKILLS", "LOCATION", "CERTIFICATION"])
                keyword = gradio.Text(label="ENTER THE SEARCH DATA")
            with gradio.Row():
                submit = gradio.Button(value="SEARCH THE DATABASE")
        with gradio.Row():
            submit.click(fn=searchByParameters, inputs=[
                parameter, keyword], outputs=[gradio.HTML()])
