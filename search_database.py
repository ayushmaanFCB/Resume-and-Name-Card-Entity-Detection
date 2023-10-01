import gradio
import re
from mongodb_connect import searchFromDB


def searchResumes(parameter, keyword):
    results = searchFromDB(parameter, keyword)
    flag = False
    output = """"""
    for result in results:
        name = result['Key Points']['basics']['name'][0]
        phone = result['Key Points']['basics']['phone']
        email = result['Key Points']['basics']['email']
        skills = result['Key Points']['expertise']['skill']
        output = output + \
            "<h1>{0}</h1><h3>PHONE : {1}</h3><h3>EMAIL : {2}</h3><h3>SKILLS : </h3>".format(
                name, ", ".join(map(str, phone)),  ", ".join(map(str, email)))
        for skill in skills:
            output = output + "\t".format(skill)

    # if flag == False:
    #     output = """<h1> Sorry, No such record exists in the database </h1>"""
    return output


with gradio.Blocks() as block:
    with gradio.Tab(label="SEARCH FOR UPLOADED RESUMES") as tab1:
        parameter = gradio.Radio(choices=["NAME", "ID", "EMAIL", "PHONE"])
        keyword = gradio.Text(label="Enter the value")
        submit = gradio.Button(value="SEARCH")
        submit.click(fn=searchResumes, inputs=[
                     parameter, keyword], outputs=[gradio.HTML()])
