import gradio
import re
from scripts.mongodb_connect import searchFromDB


def searchResumes(parameter, keyword):
    flag = False
    counter = 0

    if len(keyword) > 3:
        results = searchFromDB(parameter, keyword)
        output = """<div>"""
        for result in results:
            flag = True
            counter = counter + 1
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
            experiences = result['Key Points']['work']['experience']
            roles = result['Key Points']['work']['role']

            phone, email, languages, locations = [
                "-" if not data else data for data in (phone, email, languages, locations)]
            output = output + \
                """<h1 style='text-align:center'>{0}</h1> <table style='margin-right:auto; margin-left:auto'><tr><th>ID</th><th>CONTACT NUMBER</th><th>EMAIL IDs</th><th>LOCATIONS</th><th>LANGUAGES</th></tr>""".format(
                    name.upper())
            output = output + """<tr><tr><td><a href='/applicant/{0}' style='color:yellow'>{0}</a></td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>""".format(
                id, ", ".join(map(str, phone)), ", ".join(map(str, email)), ", ".join(
                    map(str, locations)), ", ".join(map(str, languages))
            )
            output = output + "</table>"

            datas = [companies, positions, skills, urls]
            messages = ["<h2>Companies worked at : </h2>", "<h2>Job Designations / Positions : </h2>",
                        "<h2>Applicant Skillset : </h2>", "<h2>Profile reference links : </h2>"]
            for i, data in enumerate(datas):
                if data != []:
                    output = output + "<h2>{0}</h2>".format(messages[i])
                    for info in data:
                        output = output + \
                            "<span style='margin-right: 30px'>{0}</span>".format(
                                info)

            output = output + \
                f"<br><br><p style='text-align:center'><b><i>In order to fetch complete information, Click <a href='/applicant/{id}' style='color:yellow'>here</a></b></i></p>"

            if counter > 1:
                output = output + "<hr>"

    if flag == False:
        output = """
            <div style='text-align:center; margin: 0 auto;'>
            <img style='margin: 0 auto;' width="96" height="96" src="https://img.icons8.com/color-glass/96/user-not-found.png" alt="user-not-found"/>
            <h1 style='color:red'>Sorry, No match has been found. Check the details entered.</h1>
            </div>
        """
    else:
        output = f"<h1 style='color:#7ffe01'>Matches Found : {counter}</h1>" + output

    output = output + "</div>"
    return output


def searchByParameters(parameter, keyword):
    flag = False
    results = searchFromDB(parameter, keyword)
    output = """<div>"""
    output = output + \
        """<table style='margin-right:auto; margin-left:auto'><tr><th>ID</th><th>NAME</th><th>CONTACT NUMBER</th><th>EMAIL IDs</th><th>COMPANIES</th><th>POSITION</th><th>LOCATIONS</th><th>LANGUAGES</th></tr>"""
    for result in results:
        flag = True
        id = result["_id"]
        try:
            name = result['Key Points']['basics']['name'][0]
        except:
            name = "NA"
        phone = result['Key Points']['basics']['phone']
        email = result['Key Points']['basics']['email']
        languages = result['Key Points']['basics']['language']
        locations = result['Key Points']['basics']['location']
        companies = result['Key Points']['work']['company']
        positions = result['Key Points']['work']['position']
        phone, email, languages, locations, companies, positions, locations, languages = [
            "-" if not data else data for data in (phone, email, languages, locations, companies, positions, locations, languages)]
        output = output + """<tr><tr><td><a href='/applicant/{0}' style='color:yellow'>{0}</a></td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td></tr>""".format(
            id, name, ", ".join(map(str, phone)), ", ".join(map(str, email)), ", ".join(map(str, companies)), ", ".join(
                map(str, positions)), ", ".join(map(str, locations)), ", ".join(map(str, languages))
        )
    output = output + "</table>"

    if flag == False:
        output = """
            <div style='text-align:center; margin: 0 auto;'>
            <img style='margin: 0 auto;' width="96" height="96" src="https://img.icons8.com/color-glass/96/user-not-found.png" alt="user-not-found"/>
            <h1 style='color:red'>Sorry, No such record exists. Check the details entered.</h1>
            </div>
        """
    else:
        output = "<h1 style='text-align:center'>RECORDS FETCHED</h1>" + output
    return output


with gradio.Blocks(theme=gradio.themes.Monochrome()) as block:
    with gradio.Row():
        gradio.HTML(
            "<h1 style='text-align:center; font-size:40px'>DATABASE QUERYING - Empowering Insights and Navigating Data<h1>")

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
                                            choices=["SKILL", "COURSE", "POSITION", "EXPERIENCE", "COMPANY", "LOCATION", "CERTIFICATION"])
                keyword = gradio.Text(label="ENTER THE SEARCH DATA")
            with gradio.Row():
                submit = gradio.Button(value="SEARCH THE DATABASE")
        with gradio.Row():
            submit.click(fn=searchByParameters, inputs=[
                parameter, keyword], outputs=[gradio.HTML()])
