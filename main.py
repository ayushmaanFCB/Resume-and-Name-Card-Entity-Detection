import gradio
import spacy
from spacy import displacy
import json

from scripts.text_from_pdf import extractFromPDF

try:
    resume_nlp = spacy.load("./model_Docanno30")
    print("\nModel Loaded Successfully.......... Launching Gradio App")
except Exception as e:
    print(e)


def resume_ner(filePath):
    text = extractFromPDF(filePath)
    doc = resume_nlp(text)

    with open("./assets/label_config.json", "r") as file:
        datas = json.load(file)
    color_schemes = {}
    for data in datas:
        color_schemes.update({data['text']: data['backgroundColor']})

    output = displacy.render(doc, style="ent", page=True, options={
                             "colors": color_schemes})

    html = "<h1 style='text-align:center'>Detected Entities</h1><div style='max-width:100%; overflow:auto'>" + \
        output + "</div><hr>"

    return html


with gradio.Blocks() as block:
    with gradio.Row():
        gradio.HTML(
            "<h1 style='text-align:center; font-size:40px'>Entity Recognition from Resume using Custom Trained Model</h1><hr>")
    with gradio.Row():
        with gradio.Column():
            upload_button = gradio.UploadButton(
                "Click to Upload a Resume File", file_count="single")
    with gradio.Row():
        upload_button.upload(resume_ner, upload_button, gradio.HTML(
        ), show_progress=True, scroll_to_output=True)


block.launch()


# iface = gradio.Interface(
#     fn=resume_ner,
#     inputs=gradio.File(label="Upload Resume Document"),
#     outputs=gradio.HTML(label="Detected Entities")
# )
# iface.launch()
