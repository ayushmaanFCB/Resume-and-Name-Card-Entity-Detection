import gradio
import re
from mongodb_connect import searchFromDB


def search(parameter, keyword):
    results = searchFromDB(parameter, keyword)
    flag = False
    output = """"""
    for result in results:
        if result['Key Points']['basics']['name'] != None:
            flag = True
            
    if flag == False:
        output = """# Sorry, No such record exists in the database"""
    return output


with gradio.Blocks() as block:
    with gradio.Tab(label="SEARCH FOR UPLOADED RESUMES") as tab1:
        parameter = gradio.Radio(choices=["NAME", "ID", "EMAIL", "PHONE"])
        keyword = gradio.Text(label="Enter the value")
        submit = gradio.Button(value="SEARCH")
        submit.click(fn=search, inputs=[
                     parameter, keyword], outputs=[gradio.Markdown()])
