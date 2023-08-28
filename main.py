import gradio
import spacy
from spacy import displacy

# resume_nlp = spacy.load("./ner_resumes/model-best")


def resume_ner(text):
    # doc = resume_nlp(text)
    doc = ""

    color_schemes = {
        "College Name": "red",
        "Companies worked at": "pink",
        "Degree": "yellow",
        "Designation": "orange",
        "Email Address": "cyan",
        "Graduation Year": "green",
        "Location": "magenta",
        "Name": "blue",
        "Skills": "green",
        "Years of Experience": "purple"
    }

    output = displacy.render(doc, style="ent", page=True, options={
                             "colors": color_schemes})
    html = "<div style='max-width:100%; overflow:auto'>" + output + "</div>"

    return html


def file_process(file):
    print(file)


iface = gradio.Interface(
    fn=file_process,
    inputs=gradio.inputs.File(label="Upload Resume Document"),
    outputs=gradio.HTML(label="Detected Entities")
)


iface.launch()
