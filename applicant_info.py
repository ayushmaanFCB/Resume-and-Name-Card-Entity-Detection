import gradio as gr
from mongodb_connect import searchFromDB


def echo(request: gr.Request):
    id = ""
    if request:
        print("Request headers dictionary:", request.headers)
        id = request.headers['referer'].split('/')[-2]
        print("IP address:", request.client.host)
        print("Query parameters:", dict(request.query_params))
    return id


def searchResumes(request: gr.Request):
    id = ""
    if request:
        id = request.headers['referer'].split('/')[-2]
    print(id)
    results = searchFromDB("id", id)
    output = """<div>"""
    for result in results:
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
        output = output + """<tr><tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>""".format(
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

        datas = [experiences, roles]
        messages = ["<h2>Work Experiences and Expertise : </h2>",
                    "<h2>Roles and Tasks performed : </h2>"]
        for i, data in enumerate(datas):
            if data != []:
                output = output + "<h2>{0}</h2><ul>".format(messages[i])
                for info in data:
                    output = output + \
                        "<li>{0}</li>".format(
                            info)
                output = output + "</ul>"

    output = output + "</div>"
    return output


block = gr.Interface(searchResumes, inputs=[], outputs=[
                     gr.HTML()], live=True, theme=gr.themes.Monochrome(), title="Applicant Data")
